import Button from './elements/Button';
import Input from './elements/Input'
import { useState } from 'react';

function InputPanel({ sendReq, resetAll, loading }) {
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


            <div className="flex flex-col self-start">
                <div className="flex-1 mb-4 bg-white p-6 rounded-xl border border-black/10">
                    <h3 className='text-2xl font-bakh-bold mb-7'>📝 ورودی ها سیستم</h3>
                    <div className='space-y-2'>
                        {
                            data.map((item) => (<Input key={item.id} {...item} setValue={setValue} />))
                        }
                    </div>

                    <div className='bg-blue-50 border-blue-300 border-2 rounded-lg px-6 py-4 flex items-center gap-x-2 mt-6'>
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-lightbulb size-5 text-blue-600 mt-0.5"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"></path><path d="M9 18h6"></path><path d="M10 22h4"></path></svg>
                        <p className='text-blue-800'> همه ورودی‌ها عددی هستند؛ سیستم آن‌ها را به دانش کیفی تبدیل می‌کند</p>
                    </div>
                </div>

                <div className="flex flex-col md:flex-row gap-4">
                    <Button label= {!loading ? "تحلیل و تولید پیشنهادات" : "در حال تحلیل..."} type="search" className='w-full md:flex-7' onClick={() => sendReq(data)} disabled={loading}/>
                    <Button label="بازنشانی" type="reset" className='w-full md:flex-3' onClick={() => {resetData(); resetAll()}}/>
                </div>
            </div>
        </>
    )
}

export default InputPanel