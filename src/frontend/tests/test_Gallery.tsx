import '@testing-library/jest-dom';
import React from "react";
import { render, waitFor, screen } from "@testing-library/react";
import Gallery from "../src/components/Gallery";
import { QueryClient, QueryClientProvider } from "react-query";
import api from "../src/api";
import { usePhotoStore } from "../src/store";

// Мокируем API (axios)
jest.mock("../src/api", () => ({
  __esModule: true,
  default: {
    get: jest.fn(),
  },
}));

const queryClient = new QueryClient();

describe("Gallery Component", () => {
  afterEach(() => {
    jest.clearAllMocks();
    // Очищаем Zustand-хранилище
    usePhotoStore.setState({ photos: [] });
  });

  it("отображает фотографии, полученные с API", async () => {
    const mockPhotos = [
      { id: 1, image: "http://fakeurl.com/photo1.jpg", status: "processed" },
      { id: 2, image: "http://fakeurl.com/photo2.jpg", status: "processing", progress: 70 },
    ];
    (api.get as jest.Mock).mockResolvedValueOnce({ data: mockPhotos });

    render(
      <QueryClientProvider client={queryClient}>
        <Gallery />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(api.get).toHaveBeenCalledWith("/photos/");
    }, { timeout: 5000 });

    await waitFor(() => {
      for (const photo of mockPhotos) {
        expect(screen.getByAltText(`Фото ${photo.id}`)).toBeInTheDocument();
        expect(screen.getByText(new RegExp(photo.status, "i"))).toBeInTheDocument();
      }
    }, { timeout: 5000 });

    // Проверяем, что фотографии рендерятся
    for (const photo of mockPhotos) {
      expect(screen.getByAltText(`Фото ${photo.id}`)).toBeInTheDocument();
      expect(screen.getByText(new RegExp(photo.status, "i"))).toBeInTheDocument();
    }
  });
});