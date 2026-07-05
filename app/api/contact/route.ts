import { Resend } from "resend";
import { NextRequest, NextResponse } from "next/server";

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(req: NextRequest) {
  const body = await req.json();
  const { name, email, message } = body as {
    name: string;
    email: string;
    message: string;
  };

  if (!name || !email || !message) {
    return NextResponse.json({ error: "Missing fields" }, { status: 400 });
  }

  try {
    await resend.emails.send({
      from: `Euromar Web <${process.env.RESEND_FROM_EMAIL}>`,
      to: process.env.ADMIN_NOTIFICATION_EMAIL!,
      subject: `Nuevo contacto de ${name} — euromar.com.ar`,
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
          <div style="background: #0a1e3d; color: white; padding: 24px; border-radius: 8px 8px 0 0;">
            <h2 style="margin: 0; font-size: 20px;">Nuevo mensaje desde euromar.com.ar</h2>
          </div>
          <div style="background: #f8fafc; padding: 24px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 8px 8px;">
            <p><strong>Nombre:</strong> ${name}</p>
            <p><strong>Email:</strong> <a href="mailto:${email}">${email}</a></p>
            <p><strong>Mensaje:</strong></p>
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 6px; padding: 16px; white-space: pre-wrap;">${message}</div>
          </div>
        </div>
      `,
      replyTo: email,
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("Resend error:", error);
    return NextResponse.json({ error: "Failed to send" }, { status: 500 });
  }
}
