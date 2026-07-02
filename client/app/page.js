import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gray-950 text-white overflow-hidden relative font-sans">
      {/* Background Gradients */}
      <div className="absolute top-0 -left-1/4 w-[150%] h-[1000px] bg-gradient-to-br from-purple-900/40 via-blue-900/20 to-transparent blur-3xl opacity-50 -z-10 rounded-full" />
      <div className="absolute bottom-0 right-[-20%] w-[120%] h-[800px] bg-gradient-to-tl from-indigo-900/30 via-slate-900/10 to-transparent blur-3xl opacity-50 -z-10 rounded-full" />
      
      {/* Navbar */}
      <header className="flex justify-between items-center p-6 lg:px-12 relative z-10">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-500 to-purple-500 flex items-center justify-center font-bold text-lg shadow-lg shadow-blue-500/20">
            P
          </div>
          <span className="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-gray-100 to-gray-400">
            PDF-RAG AI
          </span>
        </div>
        <Link 
          href="/dashboard"
          className="px-5 py-2.5 rounded-full border border-gray-700 bg-gray-900/50 hover:bg-gray-800 transition backdrop-blur-sm text-sm font-medium"
        >
          Login
        </Link>
      </header>

      {/* Hero Section */}
      <main className="flex flex-col items-center justify-center text-center px-4 pt-32 pb-24 relative z-10">
        <div className="inline-block mb-6 px-4 py-1.5 rounded-full border border-blue-500/30 bg-blue-500/10 backdrop-blur-md">
          <span className="text-xs font-semibold tracking-wider text-blue-300 uppercase">
            Powered by Gemini
          </span>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8 max-w-4xl leading-tight">
          Chat with your <br className="hidden md:block" />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400">
            PDF Documents Instantly
          </span>
        </h1>
        
        <p className="text-lg md:text-xl text-gray-400 mb-12 max-w-2xl leading-relaxed">
          Upload any PDF, ask questions, and get precise answers backed by AI. Seamlessly extract knowledge, summarize reports, and manage all your documents in one place.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4">
          <Link
            href="/dashboard"
            className="px-8 py-4 rounded-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold text-lg shadow-xl shadow-blue-900/50 transition transform hover:-translate-y-1"
          >
            Get Started Free
          </Link>
          <a
            href="#features"
            className="px-8 py-4 rounded-full border border-gray-700 bg-gray-900/50 hover:bg-gray-800 text-gray-200 font-semibold text-lg backdrop-blur-md transition"
          >
            Learn More
          </a>
        </div>
      </main>

      {/* Features Grid */}
      <section id="features" className="max-w-6xl mx-auto px-6 py-24 relative z-10 border-t border-gray-800/50">
        <div className="grid md:grid-cols-3 gap-8">
          <div className="p-8 rounded-2xl bg-gray-900/40 border border-gray-800 backdrop-blur-sm hover:bg-gray-800/60 transition">
            <div className="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center mb-6 border border-blue-500/30">
              <span className="text-2xl">⚡</span>
            </div>
            <h3 className="text-xl font-bold mb-3 text-gray-100">Instant Answers</h3>
            <p className="text-gray-400 leading-relaxed">
              Stop reading hundreds of pages. Just ask a question and our AI instantly finds the exact information you need.
            </p>
          </div>
          
          <div className="p-8 rounded-2xl bg-gray-900/40 border border-gray-800 backdrop-blur-sm hover:bg-gray-800/60 transition">
            <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mb-6 border border-purple-500/30">
              <span className="text-2xl">🧠</span>
            </div>
            <h3 className="text-xl font-bold mb-3 text-gray-100">Smart Context</h3>
            <p className="text-gray-400 leading-relaxed">
              We process your entire document and generate vector embeddings so the AI understands context perfectly.
            </p>
          </div>
          
          <div className="p-8 rounded-2xl bg-gray-900/40 border border-gray-800 backdrop-blur-sm hover:bg-gray-800/60 transition">
            <div className="w-12 h-12 bg-emerald-500/20 rounded-xl flex items-center justify-center mb-6 border border-emerald-500/30">
              <span className="text-2xl">📁</span>
            </div>
            <h3 className="text-xl font-bold mb-3 text-gray-100">Your Workspace</h3>
            <p className="text-gray-400 leading-relaxed">
              Keep track of all your uploaded PDFs in a sleek dashboard. Seamlessly switch between contexts with a single click.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
