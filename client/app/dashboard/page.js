"use client";

import axios from "axios";
import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";

// Enable credentials for all axios requests
axios.defaults.withCredentials = true;

export default function Home() {
  // Auth state
  const [user, setUser] = useState(null);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");

  // App state
  const [file, setFile] = useState(null);
  const [documentId, setDocumentId] = useState(null);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [documentsList, setDocumentsList] = useState([]);
  
  const chatEndRef = useRef(null);

  const fetchDocuments = async () => {
    try {
      const res = await axios.get("http://localhost:8000/api/documents/");
      setDocumentsList(res.data);
    } catch (err) {
      console.error("Failed to fetch documents", err);
    }
  };

  useEffect(() => {
    // Check if user is logged in
    const checkAuth = async () => {
      try {
        const res = await axios.get("http://localhost:8000/api/auth/me");
        setUser(res.data);
        await fetchDocuments();
      } catch (err) {
        setUser(null);
      } finally {
        setIsCheckingAuth(false);
      }
    };
    checkAuth();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleLogin = async (e) => {
    e?.preventDefault();
    try {
      await axios.post("http://localhost:8000/api/auth/login", {
        email,
        password,
      });
      const res = await axios.get("http://localhost:8000/api/auth/me");
      setUser(res.data);
      await fetchDocuments();
    } catch (err) {
      alert(err.response?.data?.detail || "Login failed");
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:8000/api/auth/register", {
        email,
        password,
        full_name: fullName,
      });
      await handleLogin();
    } catch (err) {
      alert(err.response?.data?.detail || "Registration failed");
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post("http://localhost:8000/api/auth/logout");
      setUser(null);
      setFile(null);
      setDocumentId(null);
      setMessages([]);
      setDocumentsList([]);
    } catch (err) {
      console.error("Logout error", err);
    }
  };

  // 📄 Upload PDF
  const handleFileChange = async (e) => {
    const selectedFile = e.target.files[0];

    if (selectedFile) {
      if (selectedFile.type !== "application/pdf") {
        alert("Only PDF files are allowed!");
        return;
      }

      const formData = new FormData();
      formData.append("file", selectedFile);

      try {
        const res = await axios.post("http://localhost:8000/api/documents/upload", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        setFile(selectedFile);
        setDocumentId(res.data.id);
        setMessages([]); // Clear chat for the new file
        await fetchDocuments(); // Refresh the documents list
      } catch (err) {
        alert(err.response?.data?.detail || "Upload failed");
        console.error(err);
      }
    }
  };

  const handleSelectDocument = (doc) => {
    setDocumentId(doc.id);
    setFile({ name: doc.filename, size: 0 }); // Mock file to display name
    setMessages([]);
  };

  // 💬 Send message
  const handleSend = async () => {
    if (!query.trim() || loading || !documentId) {
      if (!documentId) alert("Please upload a PDF first!");
      return;
    }

    const userMessage = { role: "user", text: query };
    setMessages((prev) => [...prev, userMessage]);

    const currentQuery = query;
    setQuery("");
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/api/chat", {
        document_id: documentId,
        question: currentQuery,
      });

      const aiMessage = {
        role: "ai",
        answer: res.data.answer || "No answer",
        sources: [],
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.detail || "Error generating response");
    } finally {
      setLoading(false);
    }
  };

  if (isCheckingAuth) {
    return (
      <div className="h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
        <div className="animate-pulse">Loading...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-950 text-white relative overflow-hidden font-sans">
        {/* Background Gradients */}
        <div className="absolute top-0 -left-1/4 w-[150%] h-[1000px] bg-gradient-to-br from-purple-900/30 via-blue-900/10 to-transparent blur-3xl opacity-60 -z-10 rounded-full" />
        <div className="absolute bottom-0 right-[-20%] w-[120%] h-[800px] bg-gradient-to-tl from-indigo-900/20 via-slate-900/10 to-transparent blur-3xl opacity-60 -z-10 rounded-full" />
        
        <div className="bg-gray-900/50 backdrop-blur-xl border border-gray-800 shadow-2xl rounded-3xl p-10 w-[90%] max-w-md relative z-10">
          
          <div className="flex flex-col items-center mb-8">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-blue-500 to-purple-500 flex items-center justify-center font-bold text-2xl shadow-lg shadow-blue-500/20 mb-4">
              P
            </div>
            <h2 className="text-3xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-gray-100 to-gray-400">
              {isLogin ? "Welcome Back" : "Create Account"}
            </h2>
            <p className="text-sm text-gray-500 mt-2">
              {isLogin ? "Sign in to access your workspace." : "Join us and chat with your PDFs."}
            </p>
          </div>

          <form onSubmit={isLogin ? handleLogin : handleRegister} className="space-y-5">
            {!isLogin && (
              <div>
                <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Full Name</label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  required
                  placeholder="John Doe"
                  className="w-full p-3.5 rounded-xl bg-gray-800/50 border border-gray-700 outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition placeholder-gray-600 text-gray-200"
                />
              </div>
            )}
            <div>
              <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Email Address</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="you@example.com"
                className="w-full p-3.5 rounded-xl bg-gray-800/50 border border-gray-700 outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition placeholder-gray-600 text-gray-200"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="••••••••"
                className="w-full p-3.5 rounded-xl bg-gray-800/50 border border-gray-700 outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition placeholder-gray-600 text-gray-200"
              />
            </div>
            
            <button
              type="submit"
              className="w-full py-4 mt-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 rounded-xl text-white font-semibold shadow-lg shadow-blue-500/25 transition transform hover:-translate-y-0.5"
            >
              {isLogin ? "Sign In" : "Create Account"}
            </button>
          </form>

          <div className="mt-8 text-center text-sm text-gray-400">
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-blue-400 font-medium hover:text-blue-300 transition underline decoration-blue-400/30 underline-offset-4"
            >
              {isLogin ? "Sign up" : "Sign in"}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      {/* HEADER */}
      <header className="flex justify-end items-center p-4 gap-4 h-16 bg-gray-900/50 border-b border-gray-800">
        <span className="text-sm text-gray-300">Hello, {user.full_name}</span>
        <button
          onClick={handleLogout}
          className="bg-red-600/80 hover:bg-red-500 text-white rounded-full font-medium text-sm h-10 px-4 transition"
        >
          Logout
        </button>
      </header>

      <div className="flex-1 flex overflow-hidden">
        {/* LEFT SIDE - Sidebar */}
        <div className="w-1/3 flex flex-col p-6 bg-gray-900/30 border-r border-gray-800 overflow-y-auto">
          
          <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 shadow-lg rounded-2xl p-6 w-full mb-8">
            <h2 className="text-xl font-semibold mb-4">Upload PDF</h2>
            <label className="flex flex-col items-center justify-center border-2 border-dashed border-gray-600 rounded-xl p-6 cursor-pointer hover:border-blue-400 hover:bg-gray-700/40 transition">
              <input
                type="file"
                accept="application/pdf"
                onChange={handleFileChange}
                className="hidden"
              />
              <p className="text-gray-300 text-sm">Drag & drop your PDF</p>
              <p className="text-xs text-gray-500 mt-1">or click to browse</p>
            </label>
          </div>

          <h2 className="text-xl font-semibold mb-4 text-gray-200">Your Documents</h2>
          
          {documentsList.length === 0 ? (
            <p className="text-gray-500 text-sm italic">No documents uploaded yet.</p>
          ) : (
            <div className="flex flex-col gap-3">
              {documentsList.map((doc) => {
                const isActive = doc.id === documentId;
                return (
                  <div
                    key={doc.id}
                    onClick={() => handleSelectDocument(doc)}
                    className={`p-4 rounded-xl cursor-pointer border transition-all duration-200 ${
                      isActive
                        ? "bg-blue-900/20 border-blue-500 shadow-md shadow-blue-500/10"
                        : "bg-gray-800/40 border-gray-700 hover:bg-gray-700/50 hover:border-gray-500"
                    }`}
                  >
                    <p className="text-sm font-medium text-gray-200 truncate" title={doc.filename}>
                      {doc.filename}
                    </p>
                    <div className="flex items-center gap-2 mt-2">
                      <span
                        className={`w-2 h-2 rounded-full ${
                          doc.status === "COMPLETED"
                            ? "bg-green-500"
                            : doc.status === "FAILED"
                            ? "bg-red-500"
                            : "bg-yellow-500 animate-pulse"
                        }`}
                      ></span>
                      <p className="text-xs text-gray-400 capitalize">
                        {doc.status.toLowerCase()}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* RIGHT SIDE - CHAT */}
        <div className="w-2/3 flex flex-col bg-gray-900/10">
          {/* HEADER */}
          <div className="p-6 border-b border-gray-800 flex items-center justify-between bg-gray-900/40">
            <div>
              <h2 className="text-xl font-semibold flex items-center gap-2">
                Chat with PDF 🤖
              </h2>
              {file && (
                <p className="text-xs text-gray-400 mt-1 truncate max-w-md">
                  Active Document: <span className="text-blue-400">{file.name}</span>
                </p>
              )}
            </div>
            {loading && (
              <div className="text-sm text-blue-400 animate-pulse bg-blue-900/20 px-3 py-1 rounded-full border border-blue-500/30">
                Thinking...
              </div>
            )}
          </div>

          {/* CHAT AREA */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full text-center">
                <div className="w-16 h-16 bg-gray-800 rounded-full flex items-center justify-center mb-4 border border-gray-700 shadow-lg">
                  <span className="text-2xl">📄</span>
                </div>
                <p className="text-gray-300 font-medium">
                  {documentId
                    ? "Ask anything about this document!"
                    : "Select or upload a PDF to start asking questions."}
                </p>
              </div>
            )}

            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex ${
                  msg.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[75%] px-5 py-3.5 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap shadow-md ${
                    msg.role === "user"
                      ? "bg-blue-600 text-white rounded-br-none"
                      : "bg-gray-800 border border-gray-700 text-gray-100 rounded-bl-none"
                  }`}
                >
                  {msg.role === "user" ? (
                    typeof msg.text === "string" ? (
                      msg.text
                    ) : (
                      JSON.stringify(msg.text)
                    )
                  ) : (
                    <div className="markdown-prose prose-sm max-w-none [&>p]:mb-2 [&>p:last-child]:mb-0 [&>strong]:font-bold [&>em]:italic [&>ul]:list-disc [&>ul]:ml-4 [&>ol]:list-decimal [&>ol]:ml-4">
                      <ReactMarkdown>{msg.answer}</ReactMarkdown>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {/* 🔥 LOADING ANIMATION */}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-800 border border-gray-700 px-5 py-4 rounded-2xl rounded-bl-none shadow-md flex gap-2 items-center">
                  <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></span>
                  <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-150"></span>
                  <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-300"></span>
                </div>
              </div>
            )}

            <div ref={chatEndRef} />
          </div>

          {/* INPUT */}
          <div className="p-6 border-t border-gray-800 bg-gray-900/60 backdrop-blur-md">
            <div className="flex gap-3 max-w-4xl mx-auto">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                placeholder={documentId ? "Ask something about the selected document..." : "Select a PDF to chat"}
                disabled={!documentId || loading}
                className="flex-1 p-4 rounded-xl bg-gray-800 border border-gray-700 outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 transition shadow-inner placeholder-gray-500"
              />

              <button
                onClick={handleSend}
                disabled={loading || !documentId}
                className="px-6 py-4 bg-blue-600 font-medium rounded-xl hover:bg-blue-500 transition disabled:opacity-50 shadow-lg shadow-blue-500/20 flex items-center gap-2"
              >
                <span>Send</span>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}