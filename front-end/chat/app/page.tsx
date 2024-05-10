import Header from "@/src/components/Header";
import { getServerSession } from "next-auth/next";
import GetThreadList from "./api/GetThreadList";
import { authOptions } from "./lib/next-auth/options";
import PopUpFunction from "./api/PopUpAPI";


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
    const PopupData = await PopUpFunction(user?.id);
    return {user:user, threadlist:threadlist, PopupData:PopupData}
  } else{
    const threadlist = []
    const PopupData = null
    return { user: user, threadlist: threadlist, PopupData: PopupData };
  } 
}

export default async function Page() {
  const Data = await PageAPI()
  console.log(Data);
  console.log(Data.PopupData?.CollectionList);
  return (
    <>
      <Header SessionUser={Data.user} ThreadList={Data.threadlist} PopUpData={Data.PopupData}></Header>
    </>
  );
}
