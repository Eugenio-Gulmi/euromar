import { NextRequest, NextResponse } from "next/server";

const LANGS = ["es", "en", "zh", "fr", "nl", "ar"];
const DEFAULT_LANG = "es";

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  const firstSegment = pathname.split("/")[1];
  if (LANGS.includes(firstSegment)) {
    return NextResponse.next();
  }

  const cookieLang = request.cookies.get("lang")?.value;
  if (cookieLang && LANGS.includes(cookieLang)) {
    return NextResponse.redirect(
      new URL(`/${cookieLang}${pathname === "/" ? "" : pathname}`, request.url)
    );
  }

  const acceptLang = request.headers.get("accept-language") ?? "";
  const preferred = acceptLang.split(",")[0].trim().slice(0, 2).toLowerCase();
  const detected = LANGS.includes(preferred) ? preferred : DEFAULT_LANG;

  return NextResponse.redirect(
    new URL(`/${detected}${pathname === "/" ? "" : pathname}`, request.url)
  );
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon\\.ico|images/|euromar-logo\\.).*)"],
};
