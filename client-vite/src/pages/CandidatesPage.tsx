import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Trash } from "lucide-react";
import { api } from "../lib/api";

interface Candidate {
  id: string;
  name: string;
  email: string;
  status: string;
}

export default function CandidatesPage() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const fetchCandidates = async () => {
    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        navigate("/auth/login");
        return;
      }

      const responseData = await api.getCandidates() as { items: Candidate[] };
      const data: Candidate[] = responseData.items;
      setCandidates(data);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCandidates();
  }, []);

  const handleReject = async (candidateId: string) => {
    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        navigate("/auth/login");
        return;
      }

      await api.updateCandidateStatus(candidateId, "REJECTED");
      fetchCandidates();
    } catch (e: any) {
      console.error("Failed to reject candidate:", e);
      setError(e.message);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold">Candidates List</h1>
        <p>Loading candidates...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold">Candidates List</h1>
        <p className="text-red-500">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold">Candidates List</h1>
      {candidates.length > 0 ? (
        <div className="mt-4">
          <table className="min-w-full bg-white border border-gray-200">
            <thead>
              <tr>
                <th className="py-2 px-4 border-b">Name</th>
                <th className="py-2 px-4 border-b">Email</th>
                <th className="py-2 px-4 border-b">Status</th>
                <th className="py-2 px-4 border-b">Actions</th>
              </tr>
            </thead>
            <tbody>
              {candidates.map((candidate) => (
                <tr key={candidate.id}>
                  <td className="py-2 px-4 border-b">{candidate.name}</td>
                  <td className="py-2 px-4 border-b">{candidate.email}</td>
                  <td className="py-2 px-4 border-b">{candidate.status}</td>
                  <td className="py-2 px-4 border-b">
                    <button
                      onClick={() => handleReject(candidate.id)}
                      className="text-red-600 hover:text-red-800"
                    >
                      <Trash size={20} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="mt-4">No candidates found.</p>
      )}
    </div>
  );
}