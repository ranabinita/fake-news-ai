import { useEffect, useState, type FormEvent } from "react";
import axios from "axios";
import {
  AlertCircle,
  CheckCircle2,
  LoaderCircle,
  Search,
  ShieldCheck,
} from "lucide-react";
import "./App.css";

type PredictionResult = {
  prediction: "Fake" | "Real";
  label: number;
};
type LiveNewsArticle = {
  id:number;
  title: string;
  description: string;
  source: string;
  url: string;
  image_url: string;
  published_at: string|null;
  prediction: "Fake" | "Real";
  label: number;
};
type LiveNewsResponse = {
  count: number;
  results: LiveNewsArticle[];
};

function App() {
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [liveNews, setLiveNews] = useState<LiveNewsArticle[]>([]);
  const [category, setCategory]=useState("general");
  const [newsError,setNewsError]=useState("");
  const [isNewsLoading,setIsNewsLoading]=useState(true);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setResult(null);

    if (!title.trim() && !text.trim()) {
      setError("Please enter a news title or article text.");
      return;
    }

    try {
      setIsLoading(true);

      const response = await axios.post<PredictionResult>("/api/predict/", {
        title: title.trim(),
        text: text.trim(),
      });

      setResult(response.data);
    } catch (requestError) {
      if (axios.isAxiosError(requestError)) {
        setError(
          requestError.response?.data?.error ||
            "Unable to analyze the news. Please check the backend server.",
        );
      } else {
        setError("An unexpected error occurred.");
      }
    } finally {
      setIsLoading(false);
    }
  };
  useEffect(() => {
    const fetchLiveNews = async () => {
      setIsNewsLoading(true);
      setNewsError("");
      try {
        const response = await axios.get<LiveNewsResponse>(
          "/api/live-news/",
          {
            params: {
              category,
              page_size: 10,
            },
          },
        );
        setLiveNews(response.data.results);
      } catch (requestError) {
        if (axios.isAxiosError(requestError)) {
          setNewsError(
            requestError.response?.data?.error ||
              "Unable to fetch live news.",
          );
        } else {
          setNewsError("An unexpected error occurred.");
        }
      } finally {
        setIsNewsLoading(false);
      }
    };
    
    fetchLiveNews();
  }, [category]);

  const handleClear = () => {
    setTitle("");
    setText("");
    setResult(null);
    setError("");
  };

  return (
    <main className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100">
      <div className="mx-auto max-w-4xl">
        <header className="mb-10 text-center">
          <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-indigo-500/15 text-indigo-400">
            <ShieldCheck size={34} />
          </div>

          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            AI Fake News Detector
          </h1>

          <p className="mx-auto mt-4 max-w-2xl text-slate-400">
            Enter a news headline, article content, or both to analyze it using
            our machine-learning model.
          </p>
        </header>

        <section className="rounded-3xl border border-slate-800 bg-slate-900 p-6 shadow-2xl shadow-black/20 sm:p-8">
          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label
                htmlFor="title"
                className="mb-2 block text-sm font-semibold text-slate-200"
              >
                News headline
              </label>

              <input
                id="title"
                type="text"
                value={title}
                onChange={(event) => setTitle(event.target.value)}
                placeholder="Enter the news headline"
                className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition placeholder:text-slate-600 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10"
              />
            </div>

            <div>
              <div className="mb-2 flex items-center justify-between">
                <label
                  htmlFor="text"
                  className="text-sm font-semibold text-slate-200"
                >
                  Article content
                </label>

                <span className="text-xs text-slate-500">
                  {text.length} characters
                </span>
              </div>

              <textarea
                id="text"
                value={text}
                onChange={(event) => setText(event.target.value)}
                placeholder="Paste the article content here..."
                rows={10}
                className="w-full resize-y rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition placeholder:text-slate-600 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10"
              />
            </div>

            {error && (
              <div className="mt-5 flex items-start gap-3 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-300">
                <AlertCircle className="mt-0.5 shrink-0" size={18} />
                <p>{error}</p>
              </div>
            )}

            <div className="mt-6 flex flex-col gap-3 sm:flex-row">
              <button
                type="submit"
                disabled={isLoading}
                className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 py-3 font-semibold transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isLoading ? (
                  <>
                    <LoaderCircle className="animate-spin" size={19} />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Search size={19} />
                    Analyze News
                  </>
                )}
              </button>

              <button
                type="button"
                onClick={handleClear}
                disabled={isLoading}
                className="rounded-xl border border-slate-700 px-6 py-3 font-semibold text-slate-300 transition hover:border-slate-600 hover:bg-slate-800 disabled:opacity-60"
              >
                Clear
              </button>
            </div>
          </form>
        </section>

        {result && (
          <section
            className={`mt-6 rounded-3xl border p-6 ${
              result.prediction === "Real"
                ? "border-emerald-500/30 bg-emerald-500/10"
                : "border-red-500/30 bg-red-500/10"
            }`}
          >
            <div className="flex items-center gap-4">
              <div
                className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-full ${
                  result.prediction === "Real"
                    ? "bg-emerald-500/20 text-emerald-400"
                    : "bg-red-500/20 text-red-400"
                }`}
              >
                {result.prediction === "Real" ? (
                  <CheckCircle2 size={26} />
                ) : (
                  <AlertCircle size={26} />
                )}
              </div>

              <div>
                <p className="text-sm text-slate-400">Model prediction</p>
                <h2
                  className={`text-2xl font-bold ${
                    result.prediction === "Real"
                      ? "text-emerald-400"
                      : "text-red-400"
                  }`}
                >
                  {result.prediction} News
                </h2>
              </div>
            </div>

            <p className="mt-5 text-sm leading-6 text-slate-400">
              This result is generated by a machine-learning model and should
              not be treated as definitive fact-checking. Confirm important
              claims using reliable sources.
            </p>
          </section>
        )}
        <section className="mt-12">
  <div className="mb-6">
    <h2 className="text-3xl font-bold">Live News</h2>

    <p className="mt-2 text-slate-400">
      Current headlines analyzed by the machine-learning model.
    </p>
  </div>

  <div className="mb-6 flex flex-wrap gap-2">
    {[
      "general",
      "technology",
      "business",
      "health",
      "science",
      "sports",
      "entertainment",
    ].map((categoryName) => (
      <button
        key={categoryName}
        type="button"
        onClick={() => setCategory(categoryName)}
        className={`rounded-full px-4 py-2 text-sm font-semibold capitalize transition ${
          category === categoryName
            ? "bg-indigo-600 text-white"
            : "border border-slate-700 text-slate-400 hover:bg-slate-800"
        }`}
      >
        {categoryName}
      </button>
    ))}
  </div>

  {isNewsLoading && (
    <div className="flex items-center justify-center gap-3 py-12 text-slate-400">
      <LoaderCircle className="animate-spin" size={22} />
      Loading live news...
    </div>
  )}

  {newsError && (
    <div className="flex gap-3 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-red-300">
      <AlertCircle className="shrink-0" size={20} />
      <p>{newsError}</p>
    </div>
  )}

  {!isNewsLoading && !newsError && (
    <div className="grid gap-5 md:grid-cols-2">
      {liveNews.map((article) => (
        <article
          key={article.id}
          className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900"
        >
          {article.image_url && (
            <img
              src={article.image_url}
              alt=""
              className="h-48 w-full object-cover"
            />
          )}

          <div className="p-5">
            <div className="mb-3 flex items-center justify-between gap-3">
              <span className="text-xs font-semibold text-indigo-400">
                {article.source}
              </span>

              <span
                className={`rounded-full px-3 py-1 text-xs font-semibold ${
                  article.prediction === "Real"
                    ? "bg-emerald-500/15 text-emerald-400"
                    : "bg-red-500/15 text-red-400"
                }`}
              >
                {article.prediction}
              </span>
            </div>

            <h3 className="text-lg font-bold leading-6">
              {article.title}
            </h3>

            <p className="mt-3 text-sm leading-6 text-slate-400">
              {article.description || "No description available."}
            </p>

            {article.published_at && (
              <p className="mt-4 text-xs text-slate-500">
                {new Date(article.published_at).toLocaleString()}
              </p>
            )}

            <a
              href={article.url}
              target="_blank"
              rel="noreferrer"
              className="mt-5 inline-block text-sm font-semibold text-indigo-400 hover:text-indigo-300"
            >
              Read full article →
            </a>
          </div>
        </article>
      ))}
    </div>
  )}
</section>
      </div>
    </main>
  );
}

export default App;