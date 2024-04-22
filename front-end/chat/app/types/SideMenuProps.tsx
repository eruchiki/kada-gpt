import * as React from 'react';
import ThreadsPropsType from './ThreadProps';


type SideMenuPropsType = {
    setOpen:React.Dispatch<React.SetStateAction<boolean>>;
    open:boolean
}

type SideMenuPropsTypewithThreads = {
    setOpen:React.Dispatch<React.SetStateAction<boolean>>;
    open:boolean
    threadlist: Array<ThreadsPropsType>
}
export default SideMenuPropsType