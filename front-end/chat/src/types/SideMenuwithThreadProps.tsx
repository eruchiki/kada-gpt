
import ThreadsPropsType from './ThreadProps';


type SideMenuPropsTypewithThreads = {
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
  open: boolean;
  threadlist: Array<ThreadsPropsType>;
  userid: number;
  PopUpData: { GroupId: number; CollectionList: any } | null;
};
export default SideMenuPropsTypewithThreads