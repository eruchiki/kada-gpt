import Header from '@/src/components/Header';
import Chat from '@/src/components/Chat/Chat';
import ThreadInfoPropsType from '@/src/types/ThreadInfoProps';

export default function ThreadPage() {
  const threadlist = [{"id":1,"name":"test1"},{"id":2,"name":"test2"}]
  const ThreadInfo: ThreadInfoPropsType = {
    id: 1,
    name: "test",
    model_name: "gpt3",
    relate_num: 4,
    collections_id: 1,
    search_method: "default",
    create_user_id: 1,
    group_id: 1,
  };
  
  return (
    <>
      <Header threadlist={threadlist}></Header>
      <Chat ThreadData={ThreadInfo} />
    </>
  );
}
