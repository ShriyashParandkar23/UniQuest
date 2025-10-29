import React, { useState, useRef, useEffect } from "react";
import {
  Send,
  Bot,
  User,
  Lightbulb,
  BookOpen,
  GraduationCap,
  MapPin,
  DollarSign,
  Sparkles,
} from "lucide-react";

export default function AIChatAssistant() {
  const predefinedQuestions = [
    {
      category: "Requirements",
      icon: BookOpen,
      questions: [
        "What are the IELTS requirements for Computer Science at Stanford?",
        "What GPA do I need for Oxford Engineering?",
        "Tell me about application deadlines for Canadian universities",
      ],
    },
  
  ];

  const aiResponses = {
    default:
      "I'm UniQuest AI, your personal study abroad assistant! I can help you with university requirements, application processes, scholarships, visa information, and more. What would you like to know?",
    ielts:
      "For Computer Science at Stanford, international students typically need an IELTS score of 7.0+ with no band below 6.5. TOEFL 100+ is also accepted.",
    gpa: "Oxford Engineering typically requires a GPA of 3.7+, competitive applicants usually 3.8+. They also consider coursework rigor and research experience.",
    tuition:
      "UK tuition fees vary by university and program, from £20,000-£50,000/year depending on the university.",
    scholarships:
      "There are many scholarships including Commonwealth, Chevening, and university-specific awards for Indian students.",
    programs:
      "For AI/ML programs, consider Stanford, MIT, CMU, University of Toronto, and ETH Zurich.",
  };

  const [messages, setMessages] = useState([
    {
      id: "1",
      content: aiResponses.default,
      sender: "ai",
      timestamp: new Date(),
      suggestions: [
        "Tell me about university requirements",
        "Help me find scholarships",
        "What are the best universities for my field?",
        "Explain the application process",
      ],
    },
  ]);

  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const generateAIResponse = (userMessage) => {
    const message = userMessage.toLowerCase();
    if (message.includes("ielts") || message.includes("toefl"))
      return aiResponses.ielts;
    if (message.includes("gpa") || message.includes("grade"))
      return aiResponses.gpa;
    if (message.includes("tuition") || message.includes("fee"))
      return aiResponses.tuition;
    if (message.includes("scholarship")) return aiResponses.scholarships;
    if (
      message.includes("program") ||
      message.includes("ai") ||
      message.includes("ml") ||
      message.includes("computer science")
    )
      return aiResponses.programs;
    return "That's a great question! I recommend checking specific university websites for up-to-date info.";
  };

  const handleSendMessage = () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      content: inputValue,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsTyping(true);

    setTimeout(() => {
      const aiMessage = {
        id: (Date.now() + 1).toString(),
        content: generateAIResponse(inputValue),
        sender: "ai",
        timestamp: new Date(),
        suggestions: [
          "Tell me more about this",
          "What are the alternatives?",
          "How can I improve my chances?",
          "What documents do I need?",
        ],
      };
      setMessages((prev) => [...prev, aiMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const handleQuestionClick = (q) => setInputValue(q);
  const handleSuggestionClick = (s) => setInputValue(s);

  return (
    <div className="space-y-6 p-6 mx-40">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg p-6 text-white text-center shadow">
        <div className="flex justify-center mb-3">
          <div className="bg-white/20 p-3 rounded-full">
            <Sparkles className="h-6 w-6 text-white" />
          </div>
        </div>
        <h1 className="text-2xl font-bold mb-1">Ask UniQuest AI</h1>
        <p className="text-blue-100">
          Get instant answers about universities, applications, and scholarships
        </p>
      </div>

      <div className="grid lg:grid-cols-4 gap-6">
        {/* Sidebar */}
        <div className="bg-white shadow rounded-lg p-4">
          <h2 className="font-bold text-lg mb-3 text-gray-800">
            Quick Questions
          </h2>
          {predefinedQuestions.map((cat) => (
            <div key={cat.category} className="mb-4">
              <div className="flex items-center space-x-2 mb-2">
                <cat.icon className="h-4 w-4 text-blue-600" />
                <h4 className="font-medium text-sm text-gray-700">
                  {cat.category}
                </h4>
              </div>
              <div className="space-y-1">
                {cat.questions.map((q, i) => (
                  <button
                    key={i}
                    onClick={() => handleQuestionClick(q)}
                    className="w-full text-left text-sm text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded px-2 py-1 transition-colors"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Chat Window */}
        <div className="lg:col-span-3 bg-white shadow rounded-lg flex flex-col">
          <div className="p-4 border-b flex items-center justify-between">
            <div>
              <h2 className="font-bold text-lg flex items-center text-gray-800">
                <Bot className="h-5 w-5 mr-2 text-blue-600" /> UniQuest AI
                Assistant
              </h2>
              <p className="text-sm text-gray-500">
                Ask me anything about studying abroad!
              </p>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${
                  msg.sender === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`flex items-start space-x-2 max-w-[80%] ${
                    msg.sender === "user"
                      ? "flex-row-reverse space-x-reverse"
                      : ""
                  }`}
                >
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center shadow ${
                      msg.sender === "user"
                        ? "bg-blue-600 text-white"
                        : "bg-gradient-to-r from-blue-600 to-indigo-600 text-white"
                    }`}
                  >
                    {msg.sender === "user" ? (
                      <User className="h-4 w-4" />
                    ) : (
                      <Bot className="h-4 w-4" />
                    )}
                  </div>
                  <div
                    className={`rounded-lg p-3 shadow-sm ${
                      msg.sender === "user"
                        ? "bg-blue-600 text-white"
                        : "bg-white text-gray-900 border"
                    }`}
                  >
                    <p className="text-sm">{msg.content}</p>
                    <p
                      className={`text-xs mt-1 ${
                        msg.sender === "user"
                          ? "text-blue-100"
                          : "text-gray-500"
                      }`}
                    >
                      {msg.timestamp.toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                  </div>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="flex justify-start">
                <div className="flex items-start space-x-2">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-600 to-indigo-600 flex items-center justify-center text-white">
                    <Bot className="h-4 w-4" />
                  </div>
                  <div className="bg-white border rounded-lg p-3 flex space-x-1 shadow-sm">
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"></span>
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-300"></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef}></div>
          </div>

          {/* Suggestions */}
          {!isTyping &&
            messages[messages.length - 1]?.suggestions &&
            messages[messages.length - 1].suggestions.length > 0 && (
              <div className="p-3 border-t flex flex-wrap gap-2 bg-gray-50">
                {messages[messages.length - 1].suggestions.map((s, i) => (
                  <button
                    key={i}
                    onClick={() => handleSuggestionClick(s)}
                    className="flex items-center gap-1 text-xs px-2 py-1 border rounded bg-white hover:bg-blue-600 hover:text-white transition-all"
                  >
                    <Lightbulb className="h-3 w-3" /> {s}
                  </button>
                ))}
              </div>
            )}

          {/* Input */}
          <div className="flex p-3 border-t bg-gray-50 space-x-2">
            <input
              type="text"
              placeholder="Ask me anything..."
              className="flex-1 border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-300"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
              disabled={isTyping}
            />
            <button
              onClick={handleSendMessage}
              disabled={isTyping || !inputValue.trim()}
              className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-4 rounded hover:opacity-90 disabled:opacity-50 flex items-center justify-center"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
