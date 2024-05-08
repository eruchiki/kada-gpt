import { getServerSession } from "next-auth/next";
import { authOptions } from "../../lib/next-auth/options";
import Header from "@/src/components/Header";
import GetThread from "@/app/api/GetThread";
import Chat from "@/src/components/Chat/Chat";
import GetThreadList from "@/app/api/GetThreadList";
import GetChatHistory from "@/app/api/GetChatHistory";
import PopUpFunction from "../../api/PopUpAPI";

type SessionUser<T> = T & {
  name?: string | null | undefined;
  id?: string | null | undefined;
  email?: string | null | undefined;
  image?: string | null | undefined;
};

const PageAPI = async (ThreadId:number) => {
  const ServerSession = await getServerSession(authOptions);
  const user: SessionUser<Session.uesr> = ServerSession?.user;
  if (user) {
    const threadInfo = await GetThread(user?.id, ThreadId);
    const PopupData = await PopUpFunction(user?.id);
    const threadlist = await GetThreadList(user?.id);
    const chathistory = await GetChatHistory(user?.id, ThreadId); 
    return {
      user: user,
      threadInfo: threadInfo,
      threadlist: threadlist,
      ChatHistory: chathistory,
      PopupData: PopupData,
    };
  } else {
    const threadInfo = null;
    const PopupData = null;
    const threadlist = [];
    const chathistory = [];
    return {
      user: user,
      threadInfo: threadInfo,
      threadlist: threadlist,
      ChatHistory: chathistory,
      PopupData: PopupData,
    };
  }
};

export default async function ThreadPage({ params }: { params: { id: number } }) {
  const ThreadId = params.id;
  const Data = await PageAPI(ThreadId)
  console.log(Data)
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
      <Header SessionUser={Data.user} ThreadList={Data.threadlist} PopUpData={Data.PopupData}></Header>
      {Data.threadInfo && (
        <Chat ThreadInfo={Data.threadInfo} SessionUser={Data.user} ChatHistory={Data.ChatHistory}/>
      )}
    </>
  );
}