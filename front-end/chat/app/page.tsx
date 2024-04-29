import Header from "@/src/components/Header";
import { getServerSession } from "next-auth/next";
import GetThreadList from "./api/GetThreadList";
import { authOptions } from "./lib/next-auth/options";
import { Session } from "inspector";


type SessionUser<T> = T & {
  name?: string | null | undefined;
  id?: string | null | undefined;
  email?: string | null | undefined;
  image?: string | null | undefined;
}; 

const PageAPI = async () => {
  const ServerSession = await getServerSession(authOptions);
  const user: SessionUser<Session.uesr> = ServerSession?.user;
  if (user) {
    const threadlist = await GetThreadList(user?.id);
    return {user:user, threadlist:threadlist}
  } else{
    const threadlist = []
    return { user: user, threadlist: threadlist };
  } 
}

export default async function Page() {
  const Data = await PageAPI()
  return (
    <>
      <Header SessionUser={Data.user} ThreadList={Data.threadlist}></Header>
    </>
  );
}
