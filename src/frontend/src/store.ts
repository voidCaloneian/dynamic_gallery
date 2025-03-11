import { create } from "zustand";

interface PhotoState {
  photos: any[];
  addPhoto: (photo: any) => void;
}

export const usePhotoStore = create<PhotoState>((set) => ({
  photos: [],
  addPhoto: (photo: any) =>
    set((state: PhotoState) => ({
      photos: [photo, ...state.photos],
      addPhoto: state.addPhoto, // сохраняем ссылку на функцию
    })),
}));