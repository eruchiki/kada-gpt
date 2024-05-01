import SendMessage from "../../../api/SendMessage";
import GetChatHistory from "../../../api/GetChatHistory";

export const POST = async (request: Request) => {
  const Data = await request.json()
  const response = await SendMessage({
    create_user_id: Data.ThreadInfo.create_user_id,
    thread_id: Data.ThreadInfo.id,
    collection_id: Data.ThreadInfo.collections_id,
    relate_num: Data.ThreadInfo.relate_num,
    search_method: Data.ThreadInfo.search_method,
    model_name: Data.ThreadInfo.model_name,
    message_text: Data.prompt,
  });
  const chathisotry = await GetChatHistory(Data.userid, Data.ThreadInfo.id);
  return Response.json(chathisotry);
};
