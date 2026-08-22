import { useState } from "react";
import type { FormEvent } from "react";
import { login, ApiError } from "../lib/api";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Couldn't sign in. Check your connection and try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#EEF0F4] flex items-center justify-center px-4 relative overflow-hidden">
      {/* Ambient signature: a faint audit-trail ledger line, echoes the domain without being loud */}
      <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-[#1B2233] via-[#3552F0] to-[#1B2233]" />

      <div className="w-full max-w-[380px]">
        <div className="mb-10 flex items-center gap-2.5">
          <div className="h-9 w-9 rounded-lg bg-[#1B2233] flex items-center justify-center shadow-sm">
            <span className="text-[#7C9BFF] text-xs font-mono font-semibold">PP</span>
          </div>
          <div className="leading-tight">
            <div className="font-semibold text-[#1B2233] text-sm">ProjectPulse</div>
            <div className="font-mono text-[11px] text-[#8B93A3] tracking-wide">workspace access</div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-8 shadow-[0_1px_2px_rgba(16,24,40,0.06),0_8px_24px_-4px_rgba(16,24,40,0.08)]">
          <h1 className="text-2xl font-semibold text-[#111827] tracking-tight mb-1.5">Sign in</h1>
          <p className="text-[13px] text-[#6B7280] mb-7">Enter your credentials to access your workspace.</p>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label htmlFor="email" className="block text-[12px] font-medium text-[#374151] mb-1.5">
                Email
              </label>
              <input
                id="email"
                type="email"
                required
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-lg border border-[#D1D5DB] px-3.5 py-2.5 text-[14px] text-[#111827]
                           placeholder:text-[#9CA3AF] shadow-sm
                           focus:outline-none focus:ring-4 focus:ring-[#3552F0]/10 focus:border-[#3552F0]
                           transition-all"
                placeholder="you@company.com"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-[12px] font-medium text-[#374151] mb-1.5">
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg border border-[#D1D5DB] px-3.5 py-2.5 text-[14px] text-[#111827]
                           placeholder:text-[#9CA3AF] shadow-sm
                           focus:outline-none focus:ring-4 focus:ring-[#3552F0]/10 focus:border-[#3552F0]
                           transition-all"
                placeholder="••••••••"
              />
            </div>

            {error && (
              <div className="rounded-lg bg-[#FEF2F2] border border-[#FECACA] px-3.5 py-2.5">
                <p className="text-[13px] text-[#B91C1C]">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-[#3552F0] text-white text-[14px] font-medium py-2.5
                         shadow-[0_1px_2px_rgba(16,24,40,0.1),0_0_0_1px_rgba(53,82,240,0.2)]
                         hover:bg-[#2C44D9] disabled:opacity-60 disabled:cursor-not-allowed
                         transition-colors focus:outline-none focus:ring-4 focus:ring-[#3552F0]/20"
            >
              {loading ? "Signing in…" : "Sign in"}
            </button>
          </form>
        </div>

        <p className="text-center text-[12px] text-[#9CA3AF] mt-6 font-mono">
          multi-tenant · audit-logged · idempotent
        </p>
      </div>
    </div>
  );
}
