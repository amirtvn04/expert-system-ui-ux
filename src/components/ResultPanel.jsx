import React from 'react'

function ResultPanel() {
    return (
        <>
            <div className='bg-white p-6 rounded-xl border border-black/10 flex items-center justify-center'>

                <div class="text-center text-gray-400">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-target size-16 mx-auto mb-4 opacity-50" data-fg-ccdl2="2.22:2.4554:/src/app/components/ResultsPanel.tsx:26:11:722:54:e:Target::::::B7YE"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>

                    <p class="text-lg">منتظر تحلیل...</p>
                    <p class="text-sm mt-2">مقادیر را وارد کرده و دکمه تحلیل را بزنید</p>
                </div>
                
            </div>
        </>
    )
}

export default ResultPanel