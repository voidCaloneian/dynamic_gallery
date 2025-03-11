import React from "react";
import { useQuery } from "react-query";
import apiClient from "../api";

type Photo = {
  id: number;
  image: string;
  status: string;
  created_at: string;
};

const fetchPhotos = async (): Promise<Photo[]> => {
  const { data } = await apiClient.get<Photo[]>("/photos/");
  return data;
};

const Gallery: React.FC = () => {
  const { data, isLoading, isError } = useQuery<Photo[]>("photos", fetchPhotos, {
    refetchInterval: 5000, // обновление каждые 5 секунд
  });

  if (isLoading) return <p>Загрузка галереи...</p>;
  if (isError) return <p>Ошибка загрузки галереи.</p>;

  return (
    <div style={{ display: "flex", flexWrap: "wrap" }}>
      {data?.map((photo) => (
        <div key={photo.id} style={{ margin: "10px" }}>
          <img
            src={photo.image}
            alt={`Фото ${photo.id}`}
            style={{
              width: "200px",
              height: "200px",
              objectFit: "cover",
              border: "1px solid #ccc",
            }}
          />
          <p style={{ textAlign: "center" }}>{photo.status}</p>
        </div>
      ))}
    </div>
  );
};

export default Gallery;