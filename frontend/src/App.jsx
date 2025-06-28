import React, { useState, useEffect } from 'react';

const sampleData = [
  {
    id: 1,
    title: 'Breakthrough in Quantum Physics',
    excerpt: `
      Researchers at Cambridge University uncover new quantum effects. These findings could reshape the field of particle physics, introducing possibilities for faster quantum computing and stronger encryption. 
      The research, led by Dr. Jane Fieldman, is already generating global interest. Experts suggest the implications may extend far beyond current theory, influencing not only computation but also energy systems and secure communication protocols.
      
      In the lab tests, quantum particles behaved in previously unobserved ways. This opens the door for more controlled quantum states, which had long been considered nearly impossible. The findings were peer-reviewed and published in the Journal of Theoretical Physics earlier this month.
      
      Critics urge cautious optimism, but most agree this is a major scientific milestone. Future steps include replication of results and industry collaboration to transition theory into application. The university is also working to make its research open-access for global collaboration.
    `.repeat(20), // simulate long text
    university: 'University of Cambridge',
    date: '2025-06-27',
    image: '',
    link: 'https://www.cam.ac.uk/news/example',
  },
  {
    id: 2,
    title: 'New Sustainable Material Developed',
    excerpt: `
      A team at Oxford has developed a new biodegradable composite that could revolutionize packaging and construction. The new material is sourced from natural polymers and breaks down in less than 30 days.
      The study outlines potential use in shipping, temporary structures, and agriculture. It avoids the harmful byproducts common in synthetic plastics. 
      
      The team collaborated with manufacturers across Europe and Asia and is already piloting with eco-conscious companies. If commercialized at scale, this could help reduce plastic pollution significantly in the next decade.
    `.repeat(20),
    university: 'University of Oxford',
    date: '2025-06-25',
    image: 'https://via.placeholder.com/400x200',
    link: 'https://www.ox.ac.uk/news/example',
  },
];

export default function App() {
  const [universityFilter, setUniversityFilter] = useState('All');
  const [filtered, setFiltered] = useState(sampleData);

  const universities = ['All', ...new Set(sampleData.map((item) => item.university))];

  useEffect(() => {
    setFiltered(
      universityFilter === 'All'
        ? sampleData
        : sampleData.filter((item) => item.university === universityFilter)
    );
  }, [universityFilter]);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">University RSS Feed Blog</h1>

      <div className="max-w-xl mx-auto mb-6">
        <select
          value={universityFilter}
          onChange={(e) => setUniversityFilter(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        >
          {universities.map((uni, idx) => (
            <option key={idx} value={uni}>
              {uni}
            </option>
          ))}
        </select>
      </div>

      <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-2">
        {filtered.map((item) => (
          <div key={item.id} className="bg-white rounded-2xl shadow-md overflow-hidden">
            <img
              src={item.image || 'https://via.placeholder.com/400x200?text=No+Image'}
              alt={item.title}
              className="w-full h-48 object-cover"
            />
            <div className="p-4 max-h-[600px] overflow-y-auto">
              <h2 className="text-xl font-semibold mb-2">{item.university}: {item.title}</h2>
              <p className="text-sm text-gray-600 mb-2">{item.date}</p>
              <p className="text-gray-700 whitespace-pre-line mb-4">
                {item.excerpt.trim().slice(0, 5000)}{item.excerpt.length > 5000 ? '...' : ''}
              </p>
              <a
                href={item.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 hover:underline"
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

