import Header from "@/src/components/Header";
import { getServerSession } from "next-auth/next";
import { NextApiRequest, NextApiResponse } from "next";
import { authOptions } from "./lib/next-auth/options";

export default async function Page() {
  const session = await getServerSession(authOptions);
  console.log(session);
  const user = session?.user;
  return (
    <>
      <Header SessionUser={user}></Header>
    </>
  );
}
