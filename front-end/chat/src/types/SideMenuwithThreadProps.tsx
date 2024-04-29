
import ThreadsPropsType from './ThreadProps';


type SideMenuPropsTypewithThreads = {
    setOpen:React.Dispatch<React.SetStateAction<boolean>>;
    open:boolean
    threadlist: Array<ThreadsPropsType>
    userid: string
}
export default SideMenuPropsTypewithThreads