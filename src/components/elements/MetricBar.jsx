import React from 'react'

function MetricBar({ label, value }) {
  return (
    <>
      <div className='flex mb-2 justify-between text-base font-bakh-bold'>
        <div className='flex gap-x-2 items-center'>
          {
            label == "نمره دیده‌شدن CTA" ? <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-eye size-5 text-blue-600"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"></path><circle cx="12" cy="12" r="3"></circle></svg> : ""
          }
          {
            label == "نمره کلیک‌پذیری CTA" ? <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-mouse-pointer size-5 text-green-600"><path d="M12.586 12.586 19 19"></path><path d="M3.688 3.037a.497.497 0 0 0-.651.651l6.5 15.999a.501.501 0 0 0 .947-.062l1.569-6.083a2 2 0 0 1 1.448-1.479l6.124-1.579a.5.5 0 0 0 .063-.947z"></path></svg> : ""
          }
          {
            label == "میزان اطمینان سیستم" ? <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-target size-5 text-purple-600"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg> : ""
          }
          
          <h5>{label}</h5>
        </div>
        <p>
          {value} 
          /100
        </p>
      </div>

      <div className='h-2.5 w-full bg-gray-200 rounded-2xl'>
        <div style={{ width: `${value}%` }} className='h-2.5 bg-gray-800 rounded-2xl'>

        </div>
      </div>
    </>
  )
}

export default MetricBar