"""
PDF Report Generator for Epigenetic Age Analysis
Creates comprehensive clinical reports with visualizations
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime
from io import BytesIO
import base64

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas


class ReportGenerator:
    """
    Generates comprehensive PDF reports for epigenetic age analysis.
    """
    
    SUBSTANCE_LABELS = {
        'control': 'Kontrol',
        'alcohol': 'Alkol Kullanım Bozukluğu',
        'cocaine': 'Kokain Kullanımı',
        'opioids': 'Opioid Kullanımı',
        'methamphetamine': 'Metamfetamin Kullanımı',
        'cannabis': 'Kannabis Kullanımı',
        'polysubstance': 'Çoklu Madde Kullanımı'
    }
    
    CLOCK_DESCRIPTIONS = {
        'Horvath': 'Pan-doku epigenetik saat (353 CpG), genel biyolojik yaşı ölçer',
        'Hannum': 'Kan-spesifik epigenetik saat (71 CpG), kan dokusuna optimize',
        'PhenoAge': 'Fenotipik yaş tahmincisi (513 CpG), hastalık riski ile ilişkili',
        'GrimAge': 'Mortalite-ilişkili saat (1030 CpG), yaşam beklentisi tahmini',
        'DunedinPACE': 'Yaşlanma hızı ölçer (173 CpG), yılda biyolojik yaşlanma oranı'
    }
    
    def __init__(self):
        """Initialize the report generator"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Set up custom paragraph styles"""
        
        def safe_add_style(name, **kwargs):
            """Safely add a style, skipping if it already exists"""
            if name not in [s.name for s in self.styles.byName.values()]:
                self.styles.add(ParagraphStyle(name=name, **kwargs))
        
        safe_add_style(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1a365d')
        )
        
        safe_add_style(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#2c5282')
        )
        
        safe_add_style(
            'SubHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.HexColor('#4a5568')
        )
        
        safe_add_style(
            'CustomBodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            leading=14
        )
        
        safe_add_style(
            'SmallText',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.gray
        )
        
        safe_add_style(
            'AlertRed',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.red,
            spaceAfter=8
        )
        
        safe_add_style(
            'AlertGreen',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.green,
            spaceAfter=8
        )
    
    def _create_header(self, canvas, doc):
        """Add header to each page"""
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 9)
        canvas.setFillColor(colors.HexColor('#1a365d'))
        canvas.drawString(inch, A4[1] - 0.5*inch, "EpiClock v4.0 - Epigenetik Yaş Analizi Raporu")
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.gray)
        canvas.drawRightString(A4[0] - inch, A4[1] - 0.5*inch, 
                               f"Oluşturulma Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        canvas.line(inch, A4[1] - 0.6*inch, A4[0] - inch, A4[1] - 0.6*inch)
        canvas.restoreState()
    
    def _create_footer(self, canvas, doc):
        """Add footer to each page"""
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.gray)
        canvas.line(inch, 0.75*inch, A4[0] - inch, 0.75*inch)
        canvas.drawString(inch, 0.5*inch, "Bu rapor yalnızca bilgilendirme amaçlıdır. Klinik kararlar için uzman görüşü alınmalıdır.")
        canvas.drawRightString(A4[0] - inch, 0.5*inch, f"Sayfa {doc.page}")
        canvas.restoreState()
    
    def generate_individual_report(self,
                                    patient_info: Dict,
                                    clock_results: Dict,
                                    comparison_result: Any = None,
                                    recommendations: List[str] = None) -> bytes:
        """
        Generate individual patient report.
        
        Args:
            patient_info: Patient demographic information
            clock_results: Dictionary of clock results
            comparison_result: Reference comparison result
            recommendations: List of clinical recommendations
        
        Returns:
            PDF as bytes
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )
        
        story = []
        
        story.append(Paragraph("EPİGENETİK YAŞ ANALİZİ RAPORU", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("1. HASTA BİLGİLERİ", self.styles['SectionHeader']))
        
        patient_data = [
            ['Parametre', 'Değer'],
            ['Hasta ID', patient_info.get('patient_id', 'N/A')],
            ['Kronolojik Yaş', f"{patient_info.get('chronological_age', 'N/A')} yıl"],
            ['Cinsiyet', 'Erkek' if patient_info.get('sex') == 'M' else 'Kadın'],
            ['Örnek Tipi', patient_info.get('tissue_type', 'Kan')],
            ['Madde Maruziyeti', self.SUBSTANCE_LABELS.get(patient_info.get('substance_type', 'control'), 'Belirtilmemiş')],
            ['Analiz Tarihi', datetime.now().strftime('%d.%m.%Y')]
        ]
        
        patient_table = Table(patient_data, colWidths=[3*inch, 3*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
        ]))
        story.append(patient_table)
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("2. EPİGENETİK SAAT SONUÇLARI", self.styles['SectionHeader']))
        
        clock_data = [['Epigenetik Saat', 'Tahmin Edilen Yaş', 'Yaş İvmelenmesi (EAA)', '95% GA', 'Yorum']]
        
        for clock_name, result in clock_results.items():
            if hasattr(result, 'predicted_age'):
                pred_age = result.predicted_age
                eaa = result.age_acceleration
                ci = result.confidence_interval
                interpretation = self._get_eaa_interpretation(eaa, clock_name)
                
                clock_data.append([
                    clock_name,
                    f"{pred_age:.1f} yıl",
                    f"{eaa:+.1f} yıl",
                    f"({ci[0]:.1f}, {ci[1]:.1f})",
                    interpretation
                ])
        
        clock_table = Table(clock_data, colWidths=[1.2*inch, 1.1*inch, 1.3*inch, 1.1*inch, 1.5*inch])
        clock_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
        ]))
        story.append(clock_table)
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("Epigenetik Saat Açıklamaları:", self.styles['SubHeader']))
        for clock, desc in self.CLOCK_DESCRIPTIONS.items():
            story.append(Paragraph(f"• <b>{clock}:</b> {desc}", self.styles['BodyText']))
        
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("3. REFERANS KARŞILAŞTIRMASI", self.styles['SectionHeader']))
        
        if comparison_result:
            comp_text = f"""
            Hastanın GrimAge epigenetik yaş ivmelenmesi (EAA = {comparison_result.sample_eaa:.1f} yıl) 
            referans popülasyonun {comparison_result.percentile:.0f}. persentiline karşılık gelmektedir 
            (Z-skoru = {comparison_result.z_score:.2f}).
            
            <b>Referans İstatistikleri:</b> Ortalama = {comparison_result.reference_mean:.1f} yıl, 
            Standart Sapma = {comparison_result.reference_std:.1f} yıl
            
            <b>Yorum:</b> {comparison_result.interpretation}
            """
            story.append(Paragraph(comp_text, self.styles['BodyText']))
        else:
            story.append(Paragraph("Referans karşılaştırması mevcut değil.", self.styles['BodyText']))
        
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("4. KLİNİK DEĞERLENDİRME VE ÖNERİLER", self.styles['SectionHeader']))
        
        if recommendations:
            for rec in recommendations:
                story.append(Paragraph(f"• {rec}", self.styles['BodyText']))
        else:
            mean_eaa = np.mean([r.age_acceleration for r in clock_results.values() 
                              if hasattr(r, 'age_acceleration')])
            
            default_recs = self._generate_recommendations(mean_eaa, patient_info.get('substance_type', 'control'))
            for rec in default_recs:
                story.append(Paragraph(f"• {rec}", self.styles['BodyText']))
        
        story.append(Spacer(1, 30))
        
        story.append(Paragraph("5. YASAL UYARI", self.styles['SectionHeader']))
        disclaimer = """
        Bu rapor, DNA metilasyon verileri kullanılarak hesaplamalı yöntemlerle oluşturulmuştur. 
        Sonuçlar yalnızca bilgilendirme amaçlıdır ve tek başına klinik karar vermek için 
        kullanılmamalıdır. Tüm bulgular, uzman bir klinisyen tarafından hasta öyküsü, 
        fizik muayene ve diğer laboratuvar bulguları ile birlikte değerlendirilmelidir.
        
        Epigenetik yaş tahminleri, kullanılan algoritma, doku tipi ve teknik faktörlere 
        bağlı olarak değişkenlik gösterebilir. Bu raporda sunulan sonuçlar, validasyon 
        çalışmalarına dayanan tahmini değerlerdir.
        """
        story.append(Paragraph(disclaimer, self.styles['SmallText']))
        
        doc.build(story, onFirstPage=self._create_header, onLaterPages=self._create_header)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_batch_report(self,
                              samples_data: pd.DataFrame,
                              summary_statistics: Dict,
                              group_comparisons: pd.DataFrame = None) -> bytes:
        """
        Generate batch analysis report for multiple samples.
        
        Args:
            samples_data: DataFrame with sample results
            summary_statistics: Summary statistics dictionary
            group_comparisons: Optional group comparison results
        
        Returns:
            PDF as bytes
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )
        
        story = []
        
        story.append(Paragraph("TOPLU EPİGENETİK YAŞ ANALİZİ RAPORU", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("1. ANALİZ ÖZETİ", self.styles['SectionHeader']))
        
        summary_data = [
            ['Parametre', 'Değer'],
            ['Toplam Örnek Sayısı', str(summary_statistics.get('total_samples', 'N/A'))],
            ['Analiz Tarihi', datetime.now().strftime('%d.%m.%Y %H:%M')],
            ['Ortalama Kronolojik Yaş', f"{summary_statistics.get('mean_age', 0):.1f} yıl"],
            ['Ortalama EAA (GrimAge)', f"{summary_statistics.get('mean_eaa', 0):.1f} yıl"],
            ['EAA Standart Sapma', f"{summary_statistics.get('std_eaa', 0):.2f} yıl"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        if group_comparisons is not None and len(group_comparisons) > 0:
            story.append(Paragraph("2. GRUP KARŞILAŞTIRMALARI", self.styles['SectionHeader']))
            
            group_data = [['Madde Tipi', 'N', 'Ortalama EAA', 'Std', 'p-değeri', 'Anlamlı']]
            for _, row in group_comparisons.iterrows():
                group_data.append([
                    self.SUBSTANCE_LABELS.get(row['group'], row['group']),
                    str(row['n']),
                    f"{row['mean_eaa']:.2f}",
                    f"{row['std_eaa']:.2f}",
                    f"{row['p_value']:.4f}",
                    'Evet' if row['significant'] else 'Hayır'
                ])
            
            group_table = Table(group_data, colWidths=[1.5*inch, 0.6*inch, 1*inch, 0.8*inch, 1*inch, 0.8*inch])
            group_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
            ]))
            story.append(group_table)
            story.append(Spacer(1, 20))
        
        story.append(Paragraph("3. BİREYSEL SONUÇLAR", self.styles['SectionHeader']))
        
        if len(samples_data) <= 50:
            sample_header = ['Örnek ID', 'Yaş', 'GrimAge EAA', 'Madde Tipi', 'Risk']
            sample_rows = [sample_header]
            
            for _, row in samples_data.head(50).iterrows():
                eaa = row.get('grimage_eaa', 0)
                risk = 'Yüksek' if eaa > 5 else 'Orta' if eaa > 2 else 'Düşük'
                sample_rows.append([
                    str(row.get('sample_id', 'N/A'))[:15],
                    f"{row.get('chronological_age', 0):.0f}",
                    f"{eaa:.1f}",
                    row.get('substance_type', 'N/A')[:10],
                    risk
                ])
            
            sample_table = Table(sample_rows, colWidths=[1.3*inch, 0.7*inch, 1.1*inch, 1.2*inch, 0.8*inch])
            sample_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7fafc')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
            ]))
            story.append(sample_table)
        else:
            story.append(Paragraph(
                f"Toplam {len(samples_data)} örnek analiz edildi. Tüm sonuçlar CSV formatında dışa aktarılabilir.",
                self.styles['BodyText']
            ))
        
        doc.build(story, onFirstPage=self._create_header, onLaterPages=self._create_header)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def _get_eaa_interpretation(self, eaa: float, clock_name: str) -> str:
        """Get short interpretation for EAA value"""
        if clock_name == 'DunedinPACE':
            if eaa < -0.05:
                return 'Yavaş'
            elif eaa < 0.05:
                return 'Normal'
            elif eaa < 0.15:
                return 'Hafif Hızlı'
            else:
                return 'Hızlı'
        else:
            if eaa < -2:
                return 'Genç'
            elif eaa < 2:
                return 'Normal'
            elif eaa < 5:
                return 'Hafif İvmelenme'
            else:
                return 'Yüksek İvmelenme'
    
    def _generate_recommendations(self, mean_eaa: float, substance_type: str) -> List[str]:
        """Generate clinical recommendations based on results"""
        recommendations = []
        
        if mean_eaa > 5:
            recommendations.append("Yüksek epigenetik yaş ivmelenmesi tespit edilmiştir. Kapsamlı tıbbi değerlendirme önerilir.")
            recommendations.append("Kardiyovasküler risk faktörlerinin değerlendirilmesi düşünülmelidir.")
        elif mean_eaa > 2:
            recommendations.append("Orta düzeyde epigenetik yaş ivmelenmesi tespit edilmiştir. Yaşam tarzı müdahaleleri değerlendirilmelidir.")
        else:
            recommendations.append("Epigenetik yaş, kronolojik yaş ile uyumludur veya daha gençtir.")
        
        if substance_type != 'control':
            recommendations.append(f"{self.SUBSTANCE_LABELS.get(substance_type, substance_type)} maruziyeti ile ilişkili olarak bağımlılık tedavi seçenekleri değerlendirilmelidir.")
            recommendations.append("Madde kullanımının kesilmesi veya azaltılması, epigenetik yaş ivmelenmesini yavaşlatabilir.")
        
        recommendations.append("Sağlıklı beslenme, düzenli egzersiz ve yeterli uyku, biyolojik yaşlanmayı olumlu etkileyebilir.")
        recommendations.append("Takip değerlendirmesi için 6-12 ay sonra tekrar analiz önerilir.")
        
        return recommendations
