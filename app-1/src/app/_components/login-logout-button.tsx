"use client";

import { signIn, signOut, useSession } from "next-auth/react";

export default function LoginLogoutButton() {
  const { status } = useSession();

  if (status === "authenticated") {
    return (
      <button
        className="rounded-full bg-white/10 px-10 py-3 font-semibold no-underline transition hover:bg-white/20"
        onClick={() => signOut()}
      >
        Logout
      </button>
    );
  } else if (status === "unauthenticated") {
    return (
      <button
        className="rounded-full bg-white/10 px-10 py-3 font-semibold no-underline transition hover:bg-white/20"
        onClick={() => signIn("keycloak")}
      >
        Login
      </button>
    );
  }

  return "Loading...";
}
