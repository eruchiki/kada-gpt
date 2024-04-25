import Header from '@/src/components/Header';
import Chat from '@/src/components/Chat/Chat';

export default function ThreadPage() {
  const threadlist = [{"id":1,"name":"test1"},{"id":2,"name":"test2"}]
  return (
      <>
      <Header threadlist={threadlist}></Header>
      <Chat></Chat>
      </>
    )
}
