from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
import math

# ==================== FastAPI App ====================

app = FastAPI(
    title="سیستم خبره تحلیل UI/UX",
    description="API برای تحلیل و بهینه‌سازی صفحات لندینگ",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration - اجازه دسترسی از React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:5174",  # Vite alternative
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "*"  # برای development - در production حذف کنید
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Pydantic Models ====================

class LandingPageInput(BaseModel):
    """مدل ورودی داده‌های صفحه لندینگ"""
    cta_position_y: int = Field(default=500, description="موقعیت CTA (پیکسل از بالا)")
    cta_width: int = Field(default=200, description="عرض CTA (پیکسل)")
    cta_height: int = Field(default=50, description="ارتفاع CTA (پیکسل)")
    contrast_ratio: float = Field(default=4.5, description="نسبت کنتراست رنگی")
    whitespace_around_cta: int = Field(default=40, description="فضای خالی اطراف CTA (پیکسل)")
    scroll_depth: int = Field(default=60, description="عمق اسکرول کاربران (%)")
    cta_click_rate: float = Field(default=3.5, description="نرخ کلیک CTA (%)")
    number_of_ctas: int = Field(default=1, description="تعداد CTA در صفحه")
    cta_text_length: int = Field(default=15, description="طول متن CTA (کاراکتر)")
    time_to_cta: int = Field(default=8, description="زمان رسیدن به CTA (ثانیه)")
    clickable_elements_before_cta: int = Field(default=3, description="تعداد عناصر کلیک‌پذیر قبل از CTA")
    content_word_count: int = Field(default=300, description="تعداد کلمات محتوای صفحه")
    similar_color_elements: int = Field(default=0, description="تعداد عناصر با رنگ مشابه CTA")
    largest_other_element_size: int = Field(default=8000, description="بزرگترین عنصر دیگر (پیکسل مربع)")
    cta_mobile_width: int = Field(default=200, description="عرض CTA در موبایل (پیکسل)")
    cta_mobile_height: int = Field(default=48, description="ارتفاع CTA در موبایل (پیکسل)")
    has_loading_animation: int = Field(default=1, description="وجود انیمیشن loading (0=خیر, 1=بله)")

    class Config:
        json_schema_extra = {
            "example": {
                "cta_position_y": 500,
                "cta_width": 200,
                "cta_height": 50,
                "contrast_ratio": 4.5,
                "whitespace_around_cta": 40,
                "scroll_depth": 60,
                "cta_click_rate": 3.5,
                "number_of_ctas": 1,
                "cta_text_length": 15,
                "time_to_cta": 8,
                "clickable_elements_before_cta": 3,
                "content_word_count": 300,
                "similar_color_elements": 0,
                "largest_other_element_size": 8000,
                "cta_mobile_width": 200,
                "cta_mobile_height": 48,
                "has_loading_animation": 1
            }
        }


class ActivatedRuleResponse(BaseModel):
    """مدل پاسخ قانون فعال‌شده"""
    rule_id: str
    priority: int
    certainty: float
    conclusion: str
    explanation: str
    category: str


class AnalysisResponse(BaseModel):
    """مدل پاسخ تحلیل کامل"""
    visibility_score: int
    clickability_score: int
    overall_certainty: float
    activated_rules: List[ActivatedRuleResponse]
    recommendations: List[str]
    qualitative_inputs: Dict[str, str]
    detailed_explanation: str
    summary: Dict[str, str]


# ==================== Data Classes ====================

@dataclass
class Rule:
    """کلاس قانون در سیستم خبره"""
    id: str
    priority: int
    certainty: float
    condition: Callable
    conclusion: str
    explanation: str
    category: str


@dataclass
class ActivatedRule:
    """قانون فعال‌شده"""
    rule: Rule
    certainty: float


# ==================== Qualitative Converter ====================

class QualitativeConverter:
    """تبدیل داده‌های کمی به کیفی"""
    
    @staticmethod
    def convert_inputs(inputs: Dict) -> Dict:
        """تبدیل تمام ورودی‌ها به شکل کیفی"""
        qualitative = {}  # فقط مقادیر کیفی، نه کپی از inputs
        
        # تبدیل طول محتوا به کیفی
        words_count = inputs.get("content_word_count", 300)
        if words_count < 200:
            qualitative["content_length"] = "کوتاه"
        elif words_count < 400:
            qualitative["content_length"] = "متوسط"
        else:
            qualitative["content_length"] = "طولانی"
        
        # تبدیل وضوح متن CTA به کیفی (بر اساس طول)
        text_len = inputs.get("cta_text_length", 15)
        if text_len <= 15 and text_len > 5:
            qualitative["cta_text_clarity"] = "خوب"
        elif text_len <= 25:
            qualitative["cta_text_clarity"] = "متوسط"
        else:
            qualitative["cta_text_clarity"] = "ضعیف"
        
        # تبدیل تمایز رنگی به کیفی (بر اساس تعداد رنگ‌های مشابه)
        similar_colors = inputs.get("similar_color_elements", 0)
        if similar_colors == 0:
            qualitative["cta_color_uniqueness"] = "منحصربفرد"
        elif similar_colors <= 2:
            qualitative["cta_color_uniqueness"] = "متوسط"
        else:
            qualitative["cta_color_uniqueness"] = "مشابه"
        
        # تبدیل سلسله‌مراتب بصری (بر اساس اندازه نسبی)
        cta_width = inputs.get("cta_width", 200)
        cta_height = inputs.get("cta_height", 50)
        largest_other = inputs.get("largest_other_element_size", 150)
        
        cta_area = cta_width * cta_height
        if cta_area > largest_other * 1.5:
            qualitative["visual_hierarchy"] = "قوی"
        elif cta_area > largest_other * 1.1:
            qualitative["visual_hierarchy"] = "متوسط"
        else:
            qualitative["visual_hierarchy"] = "ضعیف"
        
        # تبدیل موبایل (بر اساس اندازه)
        mobile_width = inputs.get("cta_mobile_width", 200)
        mobile_height = inputs.get("cta_mobile_height", 48)
        if mobile_width >= 180 and mobile_height >= 48:
            qualitative["mobile_friendly"] = "بله"
        else:
            qualitative["mobile_friendly"] = "خیر"
        
        # تبدیل بازخورد بصری (بر اساس وجود انیمیشن)
        has_animation = inputs.get("has_loading_animation", 1)
        if has_animation > 0:
            qualitative["loading_feedback"] = "بله"
        else:
            qualitative["loading_feedback"] = "خیر"
        
        return qualitative


# ==================== Knowledge Base ====================

class KnowledgeBase:
    """پایگاه دانش سیستم خبره"""
    
    def __init__(self):
        self.rules = self._create_rules()
    
    def _create_rules(self) -> List[Rule]:
        """ایجاد پایگاه دانش (قوانین)"""
        return [
            # ============ قوانین CTA Visibility ============
            Rule(
                id="V1",
                priority=10,
                certainty=0.95,
                condition=lambda d: d["cta_position_y"] > 800 and d["scroll_depth"] < 50,
                conclusion="CTA در موقعیت نامناسب: زیر fold قرار دارد و کاربران به آن نمی‌رسند",
                explanation="57% کاربران تا عمق 800 پیکسل اسکرول نمی‌کنند. CTA باید در 600 پیکسل اول باشد.",
                category="visibility"
            ),
            Rule(
                id="V2",
                priority=9,
                certainty=0.90,
                condition=lambda d: d["contrast_ratio"] < 3.0,
                conclusion="کنتراست رنگی CTA بسیار ضعیف است - قابل مشاهده نیست",
                explanation="نسبت کنتراست کمتر از 3:1 باعث می‌شود CTA در پس‌زمینه گم شود.",
                category="visibility"
            ),
            Rule(
                id="V3",
                priority=8,
                certainty=0.85,
                condition=lambda d: d["whitespace_around_cta"] < 30,
                conclusion="فضای خالی اطراف CTA ناکافی است - دیده نمی‌شود",
                explanation="فضای خالی کمتر از 40 پیکسل باعث می‌شود CTA در بین عناصر گم شود.",
                category="visibility"
            ),
            Rule(
                id="V4",
                priority=7,
                certainty=0.80,
                condition=lambda d: d["number_of_ctas"] > 1,
                conclusion="وجود چند CTA باعث سردرگمی کاربر می‌شود",
                explanation="تحقیقات نشان می‌دهد وجود بیش از یک CTA، conversion را 26% کاهش می‌دهد.",
                category="visibility"
            ),
            Rule(
                id="V5",
                priority=6,
                certainty=0.75,
                condition=lambda d: d["cta_color_uniqueness"] == "مشابه",
                conclusion="رنگ CTA با سایر عناصر مشابه است - تمایز ندارد",
                explanation="CTA باید رنگی منحصربفرد و متفاوت از سایر عناصر صفحه داشته باشد.",
                category="visibility"
            ),
            Rule(
                id="V6",
                priority=5,
                certainty=0.70,
                condition=lambda d: d["visual_hierarchy"] == "ضعیف",
                conclusion="سلسله‌مراتب بصری ضعیف - CTA برجسته نیست",
                explanation="CTA باید بزرگترین و برجسته‌ترین عنصر کلیک‌پذیر صفحه باشد.",
                category="visibility"
            ),
            
            # ============ قوانین CTA Clickability ============
            Rule(
                id="C1",
                priority=10,
                certainty=0.95,
                condition=lambda d: d["cta_width"] < 180 or d["cta_height"] < 44,
                conclusion="اندازه CTA خیلی کوچک است - کلیک مشکل است",
                explanation="حداقل اندازه توصیه‌شده برای CTA: 200×50 پیکسل (موبایل: 48×48)",
                category="clickability"
            ),
            Rule(
                id="C2",
                priority=9,
                certainty=0.90,
                condition=lambda d: d["cta_text_length"] > 25,
                conclusion="متن CTA بیش‌از‌حد طولانی است",
                explanation="متن CTA باید حداکثر 2-3 کلمه باشد. از فعل امری کوتاه استفاده کنید.",
                category="clickability"
            ),
            Rule(
                id="C3",
                priority=8,
                certainty=0.85,
                condition=lambda d: d["cta_text_clarity"] == "ضعیف",
                conclusion="متن CTA واضح و انگیزه‌بخش نیست",
                explanation="از عبارات ارزش‌محور مثل 'شروع رایگان' به جای 'ثبت‌نام' استفاده کنید.",
                category="clickability"
            ),
            Rule(
                id="C4",
                priority=7,
                certainty=0.80,
                condition=lambda d: d["clickable_elements_before_cta"] > 5,
                conclusion="عناصر کلیک‌پذیر زیادی قبل از CTA وجود دارد",
                explanation="هر عنصر کلیک‌پذیر اضافی، احتمال کلیک روی CTA را 8% کاهش می‌دهد.",
                category="clickability"
            ),
            Rule(
                id="C5",
                priority=6,
                certainty=0.75,
                condition=lambda d: d["mobile_friendly"] == "خیر",
                conclusion="CTA برای موبایل بهینه نشده است",
                explanation="60% ترافیک از موبایل است. اندازه CTA در موبایل باید حداقل 48×48 پیکسل باشد.",
                category="clickability"
            ),
            Rule(
                id="C6",
                priority=5,
                certainty=0.70,
                condition=lambda d: d["loading_feedback"] == "خیر",
                conclusion="عدم وجود بازخورد بصری پس از کلیک",
                explanation="کاربر باید بلافاصله پس از کلیک، بازخورد بصری (loading، تغییر رنگ) ببیند.",
                category="clickability"
            ),
            
            # ============ قوانین ترکیبی ============
            Rule(
                id="M1",
                priority=9,
                certainty=0.88,
                condition=lambda d: d["time_to_cta"] > 12 and d["content_length"] == "طولانی",
                conclusion="زمان رسیدن به CTA بیش‌از‌حد طولانی است",
                explanation="کاربران در 8-10 ثانیه اول تصمیم می‌گیرند. محتوا را خلاصه کنید.",
                category="visibility"
            ),
            Rule(
                id="M2",
                priority=8,
                certainty=0.82,
                condition=lambda d: d["cta_click_rate"] < 2 and d["contrast_ratio"] < 4,
                conclusion="نرخ کلیک پایین به دلیل کنتراست ضعیف",
                explanation="افزایش کنتراست به 4.5:1 می‌تواند conversion را تا 35% افزایش دهد.",
                category="clickability"
            ),
            Rule(
                id="M3",
                priority=7,
                certainty=0.78,
                condition=lambda d: d["scroll_depth"] > 70 and d["cta_position_y"] < 500,
                conclusion="موقعیت CTA بهینه است - کاربران به آن می‌رسند",
                explanation="قرارگیری CTA در 500 پیکسل اول با scroll depth بالا، نشانه طراحی خوب است.",
                category="visibility"
            ),
            Rule(
                id="M4",
                priority=6,
                certainty=0.75,
                condition=lambda d: d["cta_click_rate"] > 5 and d["cta_width"] >= 200,
                conclusion="اندازه CTA مناسب است - نرخ کلیک خوب",
                explanation="اندازه مناسب CTA منجر به نرخ کلیک بالاتر شده است.",
                category="clickability"
            ),
        ]


# ==================== Inference Engine ====================

class InferenceEngine:
    """موتور استنتاج با Forward Chaining"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.activated_rules = []
        self.converter = QualitativeConverter()
    
    def forward_chaining(self, inputs: Dict) -> Dict:
        """اجرای Forward Chaining"""
        # تبدیل ورودی‌ها به کیفی
        qualitative_inputs = self.converter.convert_inputs(inputs)
        
        # اضافه کردن مقادیر عددی اصلی برای استفاده در condition ها
        full_data = {**inputs, **qualitative_inputs}
        
        self.activated_rules = []
        
        # فعال‌سازی قوانین با استفاده از داده‌های کامل
        for rule in self.kb.rules:
            try:
                if rule.condition(full_data):
                    self.activated_rules.append(
                        ActivatedRule(rule=rule, certainty=rule.certainty)
                    )
            except:
                continue
        
        # مرتب‌سازی بر اساس اولویت
        self.activated_rules.sort(key=lambda x: x.rule.priority, reverse=True)
        
        # محاسبه امتیازات
        visibility_score = self._calculate_visibility_score(inputs)
        clickability_score = self._calculate_clickability_score(inputs)
        
        # محاسبه Certainty Factor کلی
        overall_certainty = self._calculate_combined_certainty()
        
        return {
            "activated_rules": self.activated_rules,
            "visibility_score": visibility_score,
            "clickability_score": clickability_score,
            "overall_certainty": overall_certainty,
            "recommendations": self._generate_recommendations(),
            "qualitative_inputs": qualitative_inputs  # فقط کیفی‌ها
        }
    
    def _calculate_visibility_score(self, inputs: Dict) -> int:
        """محاسبه امتیاز دیده‌شدن CTA (0-100)"""
        score = 100
        
        # موقعیت CTA (30 امتیاز)
        if inputs["cta_position_y"] > 800:
            score -= 30
        elif inputs["cta_position_y"] > 600:
            score -= 15
        elif inputs["cta_position_y"] <= 400:
            score += 5
        
        # کنتراست رنگی (25 امتیاز)
        if inputs["contrast_ratio"] < 3:
            score -= 25
        elif inputs["contrast_ratio"] < 4.5:
            score -= 10
        elif inputs["contrast_ratio"] >= 7:
            score += 5
        
        # فضای خالی (20 امتیاز)
        if inputs["whitespace_around_cta"] < 30:
            score -= 20
        elif inputs["whitespace_around_cta"] < 40:
            score -= 10
        
        # تعداد CTA (15 امتیاز)
        if inputs["number_of_ctas"] > 2:
            score -= 15
        elif inputs["number_of_ctas"] > 1:
            score -= 8
        
        # تمایز رنگی (10 امتیاز)
        similar_colors = inputs.get("similar_color_elements", 0)
        if similar_colors > 2:
            score -= 10
        elif similar_colors > 0:
            score -= 5
        
        return max(0, min(100, score))
    
    def _calculate_clickability_score(self, inputs: Dict) -> int:
        """محاسبه امتیاز قابلیت کلیک CTA (0-100)"""
        score = 100
        
        # اندازه CTA (30 امتیاز)
        if inputs["cta_width"] < 180 or inputs["cta_height"] < 44:
            score -= 30
        elif inputs["cta_width"] < 200 or inputs["cta_height"] < 50:
            score -= 15
        elif inputs["cta_width"] >= 250 and inputs["cta_height"] >= 60:
            score += 5
        
        # طول متن (25 امتیاز)
        text_len = inputs["cta_text_length"]
        if text_len > 30:
            score -= 25
        elif text_len > 25:
            score -= 15
        elif text_len > 20:
            score -= 8
        elif text_len <= 15 and text_len > 5:
            score += 5
        
        # عناصر قبل از CTA (20 امتیاز)
        if inputs["clickable_elements_before_cta"] > 7:
            score -= 20
        elif inputs["clickable_elements_before_cta"] > 5:
            score -= 10
        
        # موبایل (15 امتیاز)
        mobile_width = inputs.get("cta_mobile_width", 200)
        mobile_height = inputs.get("cta_mobile_height", 48)
        if mobile_width < 180 or mobile_height < 48:
            score -= 15
        elif mobile_width < 200:
            score -= 8
        
        # بازخورد بصری (10 امتیاز)
        if inputs.get("has_loading_animation", 1) == 0:
            score -= 10
        
        return max(0, min(100, score))
    
    def _calculate_combined_certainty(self) -> float:
        """محاسبه Certainty Factor ترکیبی"""
        if not self.activated_rules:
            return 0.5
        
        # استفاده از فرمول ترکیب Certainty Factors
        cf = self.activated_rules[0].certainty
        
        for i in range(1, len(self.activated_rules)):
            cf_new = self.activated_rules[i].certainty
            
            # فرمول ترکیب CF
            if cf > 0 and cf_new > 0:
                cf = cf + cf_new * (1 - cf)
            elif cf < 0 and cf_new < 0:
                cf = cf + cf_new * (1 + cf)
            else:
                cf = (cf + cf_new) / (1 - min(abs(cf), abs(cf_new)))
        
        return round(cf, 2)
    
    def _generate_recommendations(self) -> List[str]:
        """تولید پیشنهادات نهایی"""
        recommendations = []
        
        # استخراج پیشنهادات از قوانین فعال‌شده
        for activated in self.activated_rules[:5]:  # 5 پیشنهاد برتر
            recommendations.append(activated.rule.conclusion)
        
        return recommendations


# ==================== Explanation Facility ====================

class ExplanationFacility:
    """سیستم توضیح استدلال"""
    
    @staticmethod
    def generate_explanation(results: Dict, inputs: Dict) -> str:
        """تولید توضیحات کامل"""
        explanation = "🔍 مسیر استدلال سیستم خبره:\n"
        explanation += "=" * 50 + "\n\n"
        
        # ورودی‌های کمی
        explanation += "📊 داده‌های ورودی (کمی):\n"
        explanation += f"  • موقعیت CTA: {inputs['cta_position_y']} پیکسل\n"
        explanation += f"  • اندازه CTA: {inputs['cta_width']}×{inputs['cta_height']} پیکسل\n"
        explanation += f"  • نسبت کنتراست: {inputs['contrast_ratio']}:1\n"
        explanation += f"  • فضای خالی اطراف CTA: {inputs['whitespace_around_cta']} پیکسل\n"
        explanation += f"  • عمق اسکرول: {inputs['scroll_depth']}%\n"
        explanation += f"  • نرخ کلیک: {inputs['cta_click_rate']}%\n"
        explanation += f"  • تعداد CTA: {inputs['number_of_ctas']}\n"
        explanation += f"  • طول متن CTA: {inputs['cta_text_length']} کاراکتر\n"
        explanation += f"  • تعداد کلمات محتوا: {inputs.get('content_word_count', 'N/A')}\n"
        explanation += "\n"
        
        # ورودی‌های کیفی (تبدیل شده)
        qualitative = results.get("qualitative_inputs", {})
        explanation += "🔄 داده‌های تبدیل شده (کیفی):\n"
        explanation += f"  • طول محتوا: {qualitative.get('content_length', 'N/A')}\n"
        explanation += f"  • وضوح متن CTA: {qualitative.get('cta_text_clarity', 'N/A')}\n"
        explanation += f"  • تمایز رنگی CTA: {qualitative.get('cta_color_uniqueness', 'N/A')}\n"
        explanation += f"  • سلسله‌مراتب بصری: {qualitative.get('visual_hierarchy', 'N/A')}\n"
        explanation += f"  • سازگاری موبایل: {qualitative.get('mobile_friendly', 'N/A')}\n"
        explanation += f"  • بازخورد بصری: {qualitative.get('loading_feedback', 'N/A')}\n"
        explanation += "\n"
        
        # قوانین فعال‌شده
        explanation += "⚙️ قوانین فعال‌شده (به ترتیب اولویت):\n\n"
        
        for i, activated in enumerate(results["activated_rules"], 1):
            rule = activated.rule
            explanation += f"{i}. قانون {rule.id} (اولویت: {rule.priority}, اطمینان: {rule.certainty})\n"
            explanation += f"   دسته: {'👁️ دیده‌شدن' if rule.category == 'visibility' else '👆 کلیک‌پذیری'}\n"
            explanation += f"   ➜ {rule.conclusion}\n"
            explanation += f"   💡 {rule.explanation}\n\n"
        
        if not results["activated_rules"]:
            explanation += "   ✅ هیچ مشکل جدی شناسایی نشد!\n\n"
        
        # نتایج
        explanation += "=" * 50 + "\n"
        explanation += "📈 نتایج محاسبه‌شده:\n\n"
        explanation += f"  • امتیاز دیده‌شدن (Visibility): {results['visibility_score']}/100\n"
        explanation += f"  • امتیاز کلیک‌پذیری (Clickability): {results['clickability_score']}/100\n"
        explanation += f"  • درجه اطمینان کلی (CF): {results['overall_certainty'] * 100:.0f}%\n\n"
        
        # ارزیابی کیفی
        explanation += "🎯 ارزیابی کیفی:\n"
        
        vis_quality = ExplanationFacility._get_quality_label(results['visibility_score'])
        click_quality = ExplanationFacility._get_quality_label(results['clickability_score'])
        
        explanation += f"  • دیده‌شدن CTA: {vis_quality}\n"
        explanation += f"  • کلیک‌پذیری CTA: {click_quality}\n\n"
        
        # پیشنهادات
        explanation += "=" * 50 + "\n"
        explanation += "✅ پیشنهادات اولویت‌دار:\n\n"
        
        if results['recommendations']:
            for i, rec in enumerate(results['recommendations'], 1):
                explanation += f"{i}. {rec}\n\n"
        else:
            explanation += "✨ طراحی شما عالی است! نیازی به بهبود فوری نیست.\n\n"
        
        return explanation
    
    @staticmethod
    def _get_quality_label(score: int) -> str:
        """تبدیل امتیاز به برچسب کیفی"""
        if score >= 85:
            return "عالی ✅"
        elif score >= 70:
            return "خوب ✓"
        elif score >= 50:
            return "متوسط ⚠️"
        else:
            return "ضعیف ❌"


# ==================== API Service ====================

class ExpertSystemService:
    """سرویس سیستم خبره"""
    
    def __init__(self):
        self.kb = KnowledgeBase()
        self.ie = InferenceEngine(self.kb)
        self.ef = ExplanationFacility()
    
    def analyze(self, inputs: Dict) -> Dict:
        """تحلیل و استنتاج"""
        # اجرای Forward Chaining
        results = self.ie.forward_chaining(inputs)
        
        # تولید توضیحات
        explanation = self.ef.generate_explanation(results, inputs)
        
        # تولید خلاصه
        summary = self._create_summary(results)
        
        return {
            "visibility_score": results["visibility_score"],
            "clickability_score": results["clickability_score"],
            "overall_certainty": results["overall_certainty"],
            "activated_rules": [
                {
                    "rule_id": ar.rule.id,
                    "priority": ar.rule.priority,
                    "certainty": ar.certainty,
                    "conclusion": ar.rule.conclusion,
                    "explanation": ar.rule.explanation,
                    "category": ar.rule.category
                }
                for ar in results["activated_rules"]
            ],
            "recommendations": results["recommendations"],
            "qualitative_inputs": results["qualitative_inputs"],
            "detailed_explanation": explanation,
            "summary": summary
        }
    
    def _create_summary(self, results: Dict) -> Dict:
        """ایجاد خلاصه نتایج"""
        vis_score = results['visibility_score']
        click_score = results['clickability_score']
        cf = results['overall_certainty']
        
        # محاسبه وضعیت کلی
        avg_score = (vis_score + click_score) / 2
        if avg_score >= 85:
            overall_status = "عالی - طراحی بهینه است!"
            status_emoji = "excellent"
        elif avg_score >= 70:
            overall_status = "خوب - بهبودهای جزئی لازم است"
            status_emoji = "good"
        elif avg_score >= 50:
            overall_status = "متوسط - نیاز به بهبود دارد"
            status_emoji = "medium"
        else:
            overall_status = "ضعیف - بازطراحی توصیه می‌شود"
            status_emoji = "weak"
        
        return {
            "visibility_status": self._get_quality_label(vis_score),
            "clickability_status": self._get_quality_label(click_score),
            "certainty_level": self._get_cf_label(cf),
            "overall_status": overall_status,
            "status_emoji": status_emoji,
            "average_score": str(round(avg_score, 1))  # تبدیل به string
        }
    
    def _get_quality_label(self, score: int) -> str:
        """تبدیل امتیاز به برچسب کیفی"""
        if score >= 85:
            return "عالی"
        elif score >= 70:
            return "خوب"
        elif score >= 50:
            return "متوسط"
        else:
            return "ضعیف"
    
    def _get_cf_label(self, cf: float) -> str:
        """برچسب برای CF"""
        if cf >= 0.9:
            return "بسیار بالا"
        elif cf >= 0.8:
            return "بالا"
        elif cf >= 0.6:
            return "متوسط"
        else:
            return "پایین"


# ==================== Global Service Instance ====================

expert_service = ExpertSystemService()


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """صفحه اصلی API"""
    return {
        "message": "سیستم خبره تحلیل UI/UX صفحه لندینگ",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze",
            "health": "/api/health",
            "rules": "/api/rules",
            "docs": "/docs"
        }
    }


@app.get("/api/health")
async def health_check():
    """بررسی سلامت سرویس"""
    return {
        "status": "healthy",
        "service": "UI/UX Expert System",
        "version": "1.0.0"
    }


@app.get("/api/rules")
async def get_rules():
    """دریافت لیست قوانین سیستم خبره"""
    kb = KnowledgeBase()
    rules_list = []
    
    for rule in kb.rules:
        rules_list.append({
            "id": rule.id,
            "priority": rule.priority,
            "certainty": rule.certainty,
            "conclusion": rule.conclusion,
            "explanation": rule.explanation,
            "category": rule.category
        })
    
    return {
        "total_rules": len(rules_list),
        "rules": rules_list
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_landing_page(input_data: LandingPageInput):
    """
    تحلیل صفحه لندینگ و ارائه پیشنهادات بهینه‌سازی
    
    این endpoint داده‌های کمی صفحه لندینگ را دریافت کرده و با استفاده از
    سیستم خبره مبتنی بر قواعد، تحلیل جامعی از دیده‌شدن و کلیک‌پذیری CTA ارائه می‌دهد.
    """
    try:
        # تبدیل Pydantic model به dictionary
        input_dict = input_data.model_dump()
        
        # اجرای تحلیل
        results = expert_service.analyze(input_dict)
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در تحلیل: {str(e)}")


@app.post("/api/analyze/simple")
async def analyze_simple(input_data: LandingPageInput):
    """
    نسخه ساده تحلیل - فقط امتیازات و پیشنهادات اصلی
    """
    try:
        input_dict = input_data.model_dump()
        results = expert_service.analyze(input_dict)
        
        return {
            "visibility_score": results["visibility_score"],
            "clickability_score": results["clickability_score"],
            "overall_certainty": results["overall_certainty"],
            "recommendations": results["recommendations"][:3],  # فقط 3 پیشنهاد اول
            "summary": results["summary"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در تحلیل: {str(e)}")