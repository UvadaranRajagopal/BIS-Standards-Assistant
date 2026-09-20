import { Search } from "lucide-react";
import { useState } from "react";

interface Props {
  onSearch: (query: string) => void;
  loading: boolean;
}

export default function SearchInput({ onSearch, loading }: Props) {
  const [query, setQuery] = useState("");

  const submit = (e: React.FormEvent) => {
    e.preventDefault();

    if (query.trim() && !loading) {
      onSearch(query.trim());
    }
  };

  return (
    <div className="search-box">
      <h2>What are you procuring?</h2>

      <form onSubmit={submit}>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Example: We need LED street lights for highway illumination"
          rows={4}
        />

        <button disabled={loading || !query.trim()}>
          <Search size={18} />
          {loading ? "Analyzing..." : "Analyze Standards"}
        </button>
      </form>
    </div>
  );
}