// frontend/src/App.jsx
import React, { useState, useEffect } from "react";

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading]   = useState(true);
  const [selectedUni, setSelectedUni] = useState("All");

  // Fetch from our Flask API
  useEffect(() => {
    fetch("/api/feeds")
      .then(res => {
        if (!res.ok) throw new Error(res.statusText);
        return res.json();
      })
      .then(data => setArticles(data))
      .catch(err => console.error("API error:", err))
      .finally(() => setLoading(false));
  }, []);

  // Build “All” + unique universities list
  const universities = [
    "All",
    ...Array.from(new Set(articles.map(a => a.university))).sort()
  ];

  // Filter the articles by dropdown
  const filtered =
    selectedUni === "All"
      ? articles
      : articles.filter(a => a.university === selectedUni);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <span className="text-lg">Loading…</span>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-6">
        University RSS Feed Blog
      </h1>

      {/* University filter */}
      <div className="flex justify-center mb-6">
        <select
          className="border rounded px-4 py-2"
          value={selectedUni}
          onChange={e => setSelectedUni(e.target.value)}
        >
          {universities.map(uni => (
            <option key={uni} value={uni}>
              {uni}
            </option>
          ))}
        </select>
      </div>

      {/* Articles grid */}
      <div className="grid gap-6 md:grid-cols-2">
        {filtered.map((article, idx) => (
          <div
            key={idx}
            className="border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow"
          >
            <img
              src={article.image}
              alt={article.title}
              className="w-full h-48 object-cover"
            />
            <div className="p-4">
              <h2 className="font-semibold text-xl mb-2">
                {article.university}: {article.title}
              </h2>
              <p className="text-gray-500 text-sm mb-4">
                {new Date(article.date).toLocaleDateString()}
              </p>
              <div className="prose prose-sm max-w-none mb-4">
                <p>{article.excerpt}</p>
              </div>
              <a
                href={article.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline"
              >
                Read more →
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
