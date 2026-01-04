import Input from './elements/Input'
import { useState } from 'react';

function InputPanel() {
    const initialData = [
        { label: "موقعیت CTA (پیکسل از بالا)", id: "cta_position_y", value: 500 },
        { label: "عرض CTA (پیکسل)", id: "cta_width", value: 200 },
        { label: "ارتفاع CTA (پیکسل)", id: "cta_height", value: 50 },
        { label: "نسبت کنتراست رنگی (مثال: 4.5)", id: "contrast_ratio", value: 4.5 },
        { label: "فضای خالی اطراف CTA (پیکسل)", id: "whitespace_around_cta", value: 40 },
        { label: "عمق اسکرول کاربران (%)", id: "scroll_depth", value: 60 },
        { label: "نرخ کلیک CTA (%)", id: "cta_click_rate", value: 3.5 },
        { label: "تعداد CTA در صفحه", id: "number_of_ctas", value: 1 },
        { label: "طول متن CTA (کاراکتر)", id: "cta_text_length", value: 15 },
        { label: "زمان رسیدن به CTA (ثانیه)", id: "time_to_cta", value: 8 },
        { label: "تعداد عناصر کلیک‌پذیر قبل از CTA", id: "clickable_elements_before_cta", value: 3 },
        { label: "تعداد کلمات محتوای صفحه", id: "content_word_count", value: 300 },
        { label: "تعداد عناصر با رنگ مشابه CTA", id: "similar_color_elements", value: 0 },
        { label: "بزرگترین عنصر دیگر (پیکسل مربع)", id: "largest_other_element_size", value: 8000 },
        { label: "عرض CTA در موبایل (پیکسل)", id: "cta_mobile_width", value: 200 },
        { label: "ارتفاع CTA در موبایل (پیکسل)", id: "cta_mobile_height", value: 48 },
        { label: "وجود انیمیشن loading (0=خیر, 1=بله)", id: "has_loading_animation", value: 1 }
    ]

    const [data, setData] = useState(initialData)

    const setValue = (id, value) => {
        setData(prev =>
            prev.map(item =>
                item.id === id
                    ? { ...item, value: value }
                    : item
            )
        );
    };

    const resetData = () => {
        setData([...initialData])
    }

    return (
        <>


            <div className="flex flex-col">
                <div className="flex-1 mb-4 bg-white p-6 rounded-xl border border-black/10">
                    <h3 className='text-2xl font-bakh-bold mb-3'>📝 ورودی ها سیستم</h3>
                    <div className='space-y-2'>
                        {
                            data.map((item) => (<Input key={item.id} {...item} setValue={setValue} />))
                        }
                    </div>
                </div>

                <div className="flex gap-3">
                    <button className='flex items-center justify-center gap-2 text-xl bg-green-600 w-[70%] px-5 py-3 rounded-lg font-bakh-bold text-white hover:bg-green-700 transition-colors cursor-pointer'>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                        </svg>
                        تحلیل و تولید پیشنهادات</button>
                    <button onClick={() => resetData()} className='flex items-center justify-center gap-2 text-xl border border-blue-300 text-blue-700 w-[30%] px-5 py-3 rounded-lg cursor-pointer'>
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-rotate-ccw size-5" data-fg-d3bl24="0.8:11.4884:/src/app/App.tsx:159:17:4001:32:e:RotateCcw::::::FLu"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><path d="M3 3v5h5"></path></svg>
                        بازنشانی
                    </button>
                </div>
            </div>
        </>
    )
}

export default InputPanel