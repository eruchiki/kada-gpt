import Header from "@/src/components/Header";

export default function Page() {
  const threadlist = [
    { id: 1, name: "test1" },
    { id: 2, name: "test2" },
  ];
  return (
    <>
      <Header threadlist={threadlist}></Header>
    </>
  );
}
