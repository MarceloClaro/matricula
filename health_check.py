#!/usr/bin/env python3
"""
Quick Health Check Script
Runs a fast check to ensure all critical libraries are working
"""

import sys

def quick_health_check():
    """Run a quick health check on critical libraries"""
    print("\n" + "=" * 60)
    print("  🏥 QUICK HEALTH CHECK")
    print("=" * 60 + "\n")
    
    checks_passed = 0
    checks_total = 0
    
    # Check Python version
    checks_total += 1
    if sys.version_info >= (3, 8):
        print("✅ Python version OK:", sys.version.split()[0])
        checks_passed += 1
    else:
        print("❌ Python version too old:", sys.version.split()[0])
    
    # Check critical imports
    critical_modules = [
        ('streamlit', 'Streamlit web framework'),
        ('pandas', 'Pandas data processing'),
        ('reportlab', 'PDF generation'),
        ('PIL', 'Image processing'),
        ('cv2', 'OpenCV for webcam'),
    ]
    
    for module_name, description in critical_modules:
        checks_total += 1
        try:
            __import__(module_name)
            print(f"✅ {description}")
            checks_passed += 1
        except ImportError:
            print(f"❌ {description} - NOT AVAILABLE")
    
    # Check optional modules (face recognition)
    optional_modules = [
        ('face_recognition', 'Face recognition'),
        ('tensorflow', 'TensorFlow for anti-spoofing'),
    ]
    
    face_recognition_available = False
    for module_name, description in optional_modules:
        try:
            __import__(module_name)
            print(f"✅ {description} (optional)")
            if module_name == 'face_recognition':
                face_recognition_available = True
        except ImportError:
            print(f"⚠️  {description} (optional) - NOT AVAILABLE")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"  RESULT: {checks_passed}/{checks_total} critical checks passed")
    print("=" * 60)
    
    if checks_passed == checks_total:
        print("\n✅ System is healthy and ready to use!")
        if face_recognition_available:
            print("🎉 Face recognition features are available!")
        else:
            print("ℹ️  Face recognition not available (optional)")
        print("\n   Run the system with: streamlit run app.py\n")
        return 0
    else:
        print("\n❌ System has issues - run full diagnostics:")
        print("   python test_compatibility.py\n")
        return 1

if __name__ == '__main__':
    sys.exit(quick_health_check())
