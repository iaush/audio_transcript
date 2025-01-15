export const Throttle = (fn : Function, delay : number) => {
    let isAllowed = true;
    return function(...args :any){
        if (isAllowed){
            fn(...args)
            isAllowed = false
            setTimeout(()=> {isAllowed=true}, delay)
        }
    }
}

export const Debounce = (fn : Function,delay : number) => {
    let prevEvent : any;
    return function(...args : any){
        clearTimeout(prevEvent)
        prevEvent = setTimeout(()=>{fn(...args)},delay)
    }

}