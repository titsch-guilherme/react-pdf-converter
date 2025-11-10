# Implementation Story 07: OCR Processing Engine

## Story Overview
**As a** system  
**I want** to convert uploaded PDF files into searchable PDFs using OCR technology  
**So that** users can obtain text-searchable versions of their scanned documents

## SMART Criteria

### Specific
Implement OCR processing engine using Tesseract to convert PDF pages to images, perform text recognition, and create searchable PDF output.

### Measurable
- ✅ Tesseract OCR integration functional
- ✅ PDF to image conversion working
- ✅ Text extraction and recognition accurate
- ✅ Searchable PDF generation implemented
- ✅ Progress tracking during OCR processing
- ✅ Error handling for OCR failures
- ✅ Quality optimization for different document types

### Achievable
Standard OCR implementation using established libraries (Tesseract, pdf2image, reportlab).

### Relevant
Core functionality that provides the main value proposition of the application.

### Time-bound
**Estimated Duration:** 5 days  
**Sprint:** Sprint 2  
**Priority:** Critical (Core business functionality)

## Technical Requirements

### System Dependencies
- **Tesseract OCR:** Latest stable version
- **Poppler utils:** For PDF to image conversion
- **ImageMagick:** For image processing (optional)

### Python Dependencies
- `pytesseract` ^0.3.x (Tesseract Python bindings)
- `pdf2image` ^1.17.x (PDF to image conversion)
- `Pillow` ^10.3.x (Image processing)
- `PyPDF2` ^3.0.x (PDF manipulation)
- `reportlab` ^4.3.x (PDF creation)

## Acceptance Criteria

### AC1: OCR Engine Setup
- [ ] Tesseract OCR installed and configured
- [ ] Python bindings (pytesseract) working correctly
- [ ] Language packs installed (English + configurable others)
- [ ] OCR configuration optimized for document processing
- [ ] System dependencies verified in Docker environment

### AC2: PDF to Image Conversion
- [ ] PDF pages converted to high-quality images
- [ ] Multiple page PDFs handled correctly
- [ ] Image resolution optimized for OCR accuracy
- [ ] Memory-efficient processing for large PDFs
- [ ] Error handling for corrupted or invalid PDFs

### AC3: Text Recognition and Extraction
- [ ] Accurate text extraction from document images
- [ ] Confidence scoring for OCR results
- [ ] Text positioning and layout preservation
- [ ] Multiple language support (configurable)
- [ ] Handling of various document qualities and formats

### AC4: Searchable PDF Generation
- [ ] Original PDF layout preserved
- [ ] Extracted text overlaid invisibly for searchability
- [ ] Text positioning matches original document
- [ ] PDF metadata preserved from original
- [ ] Output file size optimization

### AC5: Progress Tracking and Monitoring
- [ ] Real-time progress updates during OCR processing
- [ ] Page-by-page progress reporting
- [ ] Processing time estimation
- [ ] Resource usage monitoring
- [ ] Detailed logging for debugging

### AC6: Error Handling and Recovery
- [ ] Graceful handling of OCR failures
- [ ] Partial processing results preserved
- [ ] Retry mechanisms for transient failures
- [ ] Clear error messages for different failure types
- [ ] Fallback options for problematic pages

### AC7: Quality and Performance Optimization
- [ ] OCR accuracy optimization for different document types
- [ ] Processing speed optimization
- [ ] Memory usage optimization for large files
- [ ] Concurrent processing support
- [ ] Quality assessment and reporting

## Implementation Structure

### Core OCR Service
```python
# services/ocr_service.py
class OCRService:
    def __init__(self):
        self.tesseract_config = self._get_tesseract_config()
        self.supported_languages = ['eng', 'spa', 'fra']  # Configurable
    
    async def convert_pdf_to_searchable(
        self, 
        input_path: str, 
        output_path: str,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> OCRResult:
        """Main OCR conversion method"""
        
    async def extract_text_from_pdf(self, pdf_path: str) -> List[PageText]:
        """Extract text from PDF pages"""
        
    async def create_searchable_pdf(
        self, 
        original_pdf: str, 
        page_texts: List[PageText], 
        output_path: str
    ) -> str:
        """Create searchable PDF with extracted text"""
        
    def _get_tesseract_config(self) -> str:
        """Get optimized Tesseract configuration"""
        return '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

# models/ocr.py
class PageText(BaseModel):
    page_number: int
    text: str
    confidence: float
    bounding_boxes: List[TextBox]
    processing_time: float

class TextBox(BaseModel):
    text: str
    x: int
    y: int
    width: int
    height: int
    confidence: float

class OCRResult(BaseModel):
    success: bool
    total_pages: int
    processed_pages: int
    total_text_length: int
    average_confidence: float
    processing_time: float
    output_file_path: Optional[str] = None
    error: Optional[str] = None
```

### PDF Processing Pipeline
```python
async def process_pdf_pages(pdf_path: str, progress_callback: Callable[[int], None]) -> List[PageText]:
    """Convert PDF pages to images and extract text"""
    
    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=300, fmt='PNG')
    total_pages = len(images)
    page_texts = []
    
    for i, image in enumerate(images):
        try:
            # Preprocess image for better OCR
            processed_image = preprocess_image(image)
            
            # Extract text with Tesseract
            text_data = pytesseract.image_to_data(
                processed_image, 
                output_type=pytesseract.Output.DICT,
                config=tesseract_config
            )
            
            # Process OCR results
            page_text = process_ocr_data(text_data, i + 1)
            page_texts.append(page_text)
            
            # Update progress
            progress = int((i + 1) / total_pages * 100)
            if progress_callback:
                await progress_callback(progress)
                
        except Exception as e:
            logger.error(f"OCR failed for page {i + 1}: {str(e)}")
            # Continue with other pages
            
    return page_texts

def preprocess_image(image: Image) -> Image:
    """Optimize image for OCR processing"""
    # Convert to grayscale
    if image.mode != 'L':
        image = image.convert('L')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)
    
    # Resize if too small
    width, height = image.size
    if width < 1000:
        scale_factor = 1000 / width
        new_size = (int(width * scale_factor), int(height * scale_factor))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    return image
```

### Integration with Job Service
```python
# Update conversion_service.py
async def process_pdf_conversion(job_id: str, file_path: str, job_service: JobService):
    """Enhanced conversion with actual OCR processing"""
    try:
        await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=5)
        
        # Create progress callback
        async def progress_callback(progress: int):
            # Map OCR progress (0-100) to job progress (5-95)
            job_progress = 5 + int(progress * 0.9)
            await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=job_progress)
        
        # Perform OCR conversion
        ocr_service = OCRService()
        output_path = generate_output_path(job_id, file_path)
        
        result = await ocr_service.convert_pdf_to_searchable(
            file_path, 
            output_path, 
            progress_callback
        )
        
        if result.success:
            # Update job with download URL
            download_url = f"/api/v1/download/{job_id}"
            await job_service.update_job_with_result(job_id, output_path, download_url)
            await job_service.update_job_status(job_id, JobStatus.DONE, progress=100)
        else:
            await job_service.update_job_status(job_id, JobStatus.FAILED, error=result.error)
            
    except Exception as e:
        error_msg = f"OCR conversion failed: {str(e)}"
        await job_service.update_job_status(job_id, JobStatus.FAILED, error=error_msg)
    finally:
        # Cleanup original file
        await cleanup_temp_file(file_path)
```

## Definition of Done
- [ ] All acceptance criteria are met
- [ ] Unit tests for OCR components (>90% coverage)
- [ ] Integration tests with sample PDF files
- [ ] Performance tests with various file sizes
- [ ] Quality tests with different document types
- [ ] Error scenario testing completed
- [ ] Docker environment includes all OCR dependencies
- [ ] Code review completed and approved

## Dependencies
- **Requires:** Implementation Story 06 (Backend File Processing)
- **System Dependencies:** Tesseract OCR, Poppler utils installation
- **Integrates with:** Job management and file storage systems

## Test Scenarios

### Happy Path Tests
1. **Single Page PDF OCR**
   - Simple single-page PDF processed
   - Text extracted accurately
   - Searchable PDF generated
   - Progress updates working

2. **Multi-Page PDF OCR**
   - Complex multi-page document processed
   - All pages converted successfully
   - Text searchability verified
   - Performance within acceptable limits

3. **Various Document Types**
   - Scanned documents processed
   - Text documents with images
   - Mixed content documents
   - Different languages supported

### Error Scenarios
1. **Corrupted PDF Files**
   - Invalid PDF structure handled
   - Appropriate error messages
   - Graceful failure without system crash

2. **OCR Processing Failures**
   - Individual page failures isolated
   - Partial results preserved
   - Clear error reporting

3. **Resource Limitations**
   - Large file processing
   - Memory usage controlled
   - Timeout handling implemented

## Quality Metrics
- **Text Accuracy:** >95% for clear documents, >85% for poor quality
- **Processing Speed:** <30 seconds per page for standard documents
- **Memory Usage:** <500MB per concurrent job
- **File Size:** Output files <150% of original size

## Performance Optimization
```python
# OCR optimization configurations
TESSERACT_CONFIGS = {
    'fast': '--oem 3 --psm 6',
    'accurate': '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
    'multilang': '--oem 3 --psm 6 -l eng+spa+fra'
}

# Image preprocessing optimizations
def optimize_for_ocr(image: Image, document_type: str = 'mixed') -> Image:
    """Optimize image based on document type"""
    if document_type == 'text_heavy':
        return enhance_text_image(image)
    elif document_type == 'handwritten':
        return enhance_handwriting_image(image)
    else:
        return standard_enhancement(image)
```

## Security Considerations
- [ ] Secure handling of temporary image files
- [ ] Memory cleanup after processing
- [ ] Input validation for OCR parameters
- [ ] Resource usage limits to prevent DoS
- [ ] Secure file path handling

## Configuration
```python
class OCRSettings(BaseSettings):
    tesseract_cmd: str = '/usr/bin/tesseract'
    tesseract_config: str = '--oem 3 --psm 6'
    supported_languages: List[str] = ['eng']
    image_dpi: int = 300
    max_image_size: int = 4000  # pixels
    ocr_timeout: int = 300  # seconds
    confidence_threshold: float = 60.0
    enable_preprocessing: bool = True
```

## Risks and Mitigation
- **Risk:** OCR accuracy varies with document quality
  - **Mitigation:** Image preprocessing, multiple OCR attempts, quality assessment
- **Risk:** Processing time for large documents
  - **Mitigation:** Progress tracking, timeout handling, optimization techniques
- **Risk:** Memory usage with high-resolution images
  - **Mitigation:** Image size limits, memory monitoring, garbage collection

## Notes
- Consider implementing OCR quality assessment and user feedback
- Plan for future enhancements: custom OCR models, AI-based preprocessing
- Monitor OCR accuracy and collect metrics for continuous improvement
- Consider caching OCR results for identical documents