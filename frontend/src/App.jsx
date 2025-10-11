import "./App.css";
import Chat from "src/components/Chat";
import GlassCard from "./components/GlassCard";
import HeroBackground from "./components/HeroBackground";

function ChatApp() {
  return (
    <div className="px-4 w-full">
      <div className="mx-auto w-full max-w-3xl">
        <GlassCard className="mx-auto w-full">
          <Chat />
        </GlassCard>
      </div>
    </div>
  );
}

function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-center space-y-4">
      <HeroBackground />
      <ChatApp />
    </div>
  );
}

export default App;
