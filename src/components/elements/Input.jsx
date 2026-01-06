import React, { useId } from 'react'

function Input({id ,label, value, setValue}) {
    return (
        <div className='flex items-center justify-between'>
            <label htmlFor={id} className='text-sm text-black/70'>{label}</label>
            <input id={id} value={value} onChange={(e) => setValue(id, parseFloat(e.target.value) || 0)} dir='ltr' type="number" className='border border-black/10 rounded-lg outline-none focus:border-black/50 focus:border-2 hover:border-black/50 px-2 py-1 w-20 md:w-40' />
        </div>
    )
}

export default Input