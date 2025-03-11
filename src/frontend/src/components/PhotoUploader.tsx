import React, { useCallback, useState, useEffect } from "react";
import { useDropzone } from "react-dropzone";
import apiClient from "../api";

const PhotoUploader: React.FC = () => {
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [processingProgress, setProcessingProgress] = useState<number>(0);
  const [status, setStatus] = useState<string>("");
  // Если переменная photoId не используется нигде иначе, её можно удалить.
  // const [photoId, setPhotoId] = useState<number | null>(null);
  const [ws, setWs] = useState<WebSocket | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    const formData = new FormData();
    formData.append("image", file);

    setUploadProgress(0);
    setProcessingProgress(0);
    setStatus("Uploading");

    try {
      const response = await apiClient.post("/photos/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percent = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setUploadProgress(percent);
          }
        },
      });

      // Можно использовать идентификатор непосредственно из ответа:
      const id = response.data.id;
      setStatus("Processing");

      // Подключаемся к WebSocket для получения статуса обработки
      const wsUrl = `ws://localhost:8000/ws/photos/${id}/`;
      const socket = new WebSocket(wsUrl);
      socket.onopen = () => {
        console.log("WebSocket connected");
      };
      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "progress") {
          setProcessingProgress(data.progress);
        } else if (data.type === "completed") {
          setStatus("Completed");
          setProcessingProgress(100);
          socket.close();
        } else if (data.type === "failed") {
          setStatus("Failed: " + data.error);
          socket.close();
        }
      };
      setWs(socket);
    } catch (error) {
      console.error("Upload error", error);
      setStatus("Upload Failed");
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [] },
  });

  useEffect(() => {
    return () => {
      ws && ws.close();
    };
  }, [ws]);

  return (
    <div>
      <div
        {...getRootProps()}
        style={{
          border: "2px dashed #888",
          padding: "20px",
          textAlign: "center",
          cursor: "pointer",
        }}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Отпустите файл здесь...</p>
        ) : (
          <p>Перетащите фото для загрузки или нажмите, чтобы выбрать файл</p>
        )}
      </div>
      <div style={{ marginTop: "20px" }}>
        <p>
          <strong>Статус загрузки:</strong> {uploadProgress}%
        </p>
        {uploadProgress === 100 && (
          <>
            <p>
              <strong>Статус обработки:</strong> {processingProgress}%
            </p>
            <p>
              <strong>Общий статус:</strong> {status}
            </p>
          </>
        )}
      </div>
    </div>
  );
};

export default PhotoUploader;