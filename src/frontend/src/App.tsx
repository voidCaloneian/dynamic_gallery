import React from "react";
import { QueryClient, QueryClientProvider } from "react-query";
import PhotoUploader from "./components/PhotoUploader";
import Gallery from "./components/Gallery";

const queryClient = new QueryClient();

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <div style={{ maxWidth: "800px", margin: "0 auto", padding: "20px" }}>
        <h1 style={{ textAlign: "center" }}>Photo Upload App</h1>
        <PhotoUploader />
        <hr style={{ margin: "40px 0" }} />
        <Gallery />
      </div>
    </QueryClientProvider>
  );
};

export default App;