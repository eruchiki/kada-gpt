import { getServerSession } from "next-auth/next";
import { authOptions } from "../../lib/next-auth/options";
import Header from "@/src/components/Header";
import Chat from "@/src/components/Chat/Chat";


export default async function ThreadPage({ params }: { params: { id: number } }) {
  const ThreadId = params.id;
  const session = await getServerSession(authOptions);
  const user = session?.user;
  // const ThreadInfo = await GetThread(session?.user?.email, ThreadId);
  // try {
  //   const session = await getServerSession(authOptions);
  //   if (session) {
  //     const ThreadInfo = await GetThread(session?.user?.email, ThreadId);
  //   }
  // } catch (error) {
  //   console.error("An error occurred:", error);
  //   return { notFound: true }; 
  // }

  return (
    <>
      <Header SessionUser={user}></Header>
      <Chat ThreadId={ThreadId} SessionUser={user} />
    </>
  );
}