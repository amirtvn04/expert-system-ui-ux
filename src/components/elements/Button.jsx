import { useState } from "react"

function Button({ label, type, className, ...props }) {
    const [pressed, setPressed] = useState(false)
    const customClass = {
        reset: "hover:bg-blue-100 border-blue-300 text-blue-800",
        search: "hover:bg-green-700 bg-green-600 text-white",
    }
    
    return (
        <button {...props} onMouseDown={() => setPressed(true)} onMouseUp={() => setPressed(false)} className={`flex items-center justify-center gap-2 text-xl border px-5 py-3 rounded-lg cursor-pointer transition-all ease-out disabled:cursor-not-allowed ${pressed ? "scale-105" : "scale-100"} ${customClass[type]} ${className}`}>
            {type === "search" ?
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                </svg>
                : ""}
            {type === "reset" ?
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-rotate-ccw size-5" data-fg-d3bl24="0.8:11.4884:/src/app/App.tsx:159:17:4001:32:e:RotateCcw::::::FLu"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><path d="M3 3v5h5"></path></svg>
                : ""}
            {label}
        </button>
    )
}

export default Button