"use client";

import { signIn, useSession } from "next-auth/react";
import { redirect } from "next/navigation";

export default function Login() {
  const { status } = useSession();

  if (status === "authenticated") {
    return redirect("/");
  } else if (status === "unauthenticated") {
    void signIn("keycloak");
  }

  return "Loading...";
}
