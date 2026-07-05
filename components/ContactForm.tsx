"use client";

import { useState } from "react";
import { Send, CheckCircle, AlertCircle } from "lucide-react";

type Strings = {
  form_name: string;
  form_email: string;
  form_message: string;
  form_submit: string;
  form_sending: string;
  form_success: string;
  form_error: string;
};

export default function ContactForm({ strings }: { strings: Strings }) {
  const [form, setForm] = useState({ name: "", email: "", message: "" });
  const [status, setStatus] = useState<"idle" | "sending" | "success" | "error">("idle");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("sending");
    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (res.ok) {
        setStatus("success");
        setForm({ name: "", email: "", message: "" });
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  }

  const inputClass =
    "w-full border border-slate-200 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-navy-700 focus:border-transparent bg-white";

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1.5">
          {strings.form_name}
        </label>
        <input
          type="text"
          value={form.name}
          onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))}
          required
          className={inputClass}
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1.5">
          {strings.form_email}
        </label>
        <input
          type="email"
          value={form.email}
          onChange={(e) => setForm((p) => ({ ...p, email: e.target.value }))}
          required
          className={inputClass}
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1.5">
          {strings.form_message}
        </label>
        <textarea
          value={form.message}
          onChange={(e) => setForm((p) => ({ ...p, message: e.target.value }))}
          required
          rows={5}
          className={`${inputClass} resize-none`}
        />
      </div>

      {status === "success" && (
        <div className="flex items-center gap-2 text-green-700 bg-green-50 border border-green-200 rounded-lg px-4 py-3 text-sm">
          <CheckCircle className="w-4 h-4 shrink-0" />
          {strings.form_success}
        </div>
      )}
      {status === "error" && (
        <div className="flex items-center gap-2 text-red-700 bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-sm">
          <AlertCircle className="w-4 h-4 shrink-0" />
          {strings.form_error}
        </div>
      )}

      <button
        type="submit"
        disabled={status === "sending"}
        className="w-full bg-navy-900 hover:bg-navy-800 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2 disabled:opacity-60"
      >
        <Send className="w-4 h-4" />
        {status === "sending" ? strings.form_sending : strings.form_submit}
      </button>
    </form>
  );
}
