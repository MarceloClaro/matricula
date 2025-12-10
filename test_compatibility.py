#!/usr/bin/env python3
"""
Comprehensive Library Compatibility Test Script
Tests all libraries for compatibility, version conflicts, and deprecated features
Provides solutions and alternatives for any issues found
"""

import sys
import os
import subprocess
import importlib
import pkg_resources
from typing import Dict, List, Tuple, Optional
import warnings

# Suppress warnings during import tests
warnings.filterwarnings('ignore')

class CompatibilityTester:
    def __init__(self):
        self.results = {
            'basic': {},
            'optional': {},
            'system': {},
            'conflicts': [],
            'deprecations': [],
            'recommendations': []
        }
        self.python_version = sys.version_info
        
    def print_header(self, title: str):
        """Print a formatted header"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)
    
    def check_python_version(self):
        """Check Python version compatibility"""
        self.print_header("PYTHON VERSION CHECK")
        
        print(f"Python version: {sys.version}")
        print(f"Version info: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        
        if self.python_version < (3, 8):
            print("❌ CRITICAL: Python 3.8 or higher required")
            self.results['system']['python'] = 'INCOMPATIBLE'
            self.results['recommendations'].append(
                "CRITICAL: Upgrade to Python 3.8 or higher"
            )
            return False
        elif self.python_version >= (3, 12):
            print("⚠️  WARNING: Python 3.12+ detected - some libraries may have compatibility issues")
            print("   Recommended: Python 3.8-3.11 for best compatibility")
            self.results['system']['python'] = 'WARNING'
            self.results['recommendations'].append(
                "Consider using Python 3.8-3.11 for better compatibility"
            )
        else:
            print("✅ Python version compatible")
            self.results['system']['python'] = 'OK'
        
        return True
    
    def test_library_import(self, module_name: str, package_name: str = None) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Test if a library can be imported and get its version
        Returns: (success, version, error_message)
        """
        if package_name is None:
            package_name = module_name
        
        try:
            # Try to import the module
            module = importlib.import_module(module_name)
            
            # Try to get version
            version = None
            try:
                version = pkg_resources.get_distribution(package_name).version
            except:
                # Try alternative ways to get version
                if hasattr(module, '__version__'):
                    version = module.__version__
                elif hasattr(module, 'VERSION'):
                    version = module.VERSION
                elif hasattr(module, 'version'):
                    version = module.version
            
            return True, version, None
            
        except ImportError as e:
            return False, None, str(e)
        except Exception as e:
            return False, None, f"Unexpected error: {str(e)}"
    
    def test_basic_libraries(self):
        """Test basic required libraries"""
        self.print_header("BASIC LIBRARIES TEST")
        
        basic_libs = {
            'streamlit': 'streamlit',
            'pandas': 'pandas',
            'reportlab': 'reportlab',
            'PIL': 'pillow',
            'plotly': 'plotly',
            'cv2': 'opencv-python-headless',
            'numpy': 'numpy',
            'sklearn': 'scikit-learn',
        }
        
        for module, package in basic_libs.items():
            success, version, error = self.test_library_import(module, package)
            
            if success:
                print(f"✅ {package:<30} v{version if version else 'unknown'}")
                self.results['basic'][package] = {'status': 'OK', 'version': version}
            else:
                print(f"❌ {package:<30} FAILED: {error}")
                self.results['basic'][package] = {'status': 'FAILED', 'error': error}
        
        return all(lib['status'] == 'OK' for lib in self.results['basic'].values())
    
    def test_optional_libraries(self):
        """Test optional libraries (face recognition stack)"""
        self.print_header("OPTIONAL LIBRARIES TEST (Face Recognition)")
        
        optional_libs = {
            'dlib': 'dlib',
            'face_recognition': 'face-recognition',
            'tensorflow': 'tensorflow',
            'keras': 'tensorflow',  # Keras is now part of TensorFlow
            'imgaug': 'imgaug',
        }
        
        for module, package in optional_libs.items():
            success, version, error = self.test_library_import(module, package)
            
            if success:
                print(f"✅ {package:<30} v{version if version else 'unknown'}")
                self.results['optional'][package] = {'status': 'OK', 'version': version}
            else:
                print(f"⚠️  {package:<30} NOT AVAILABLE: {error}")
                self.results['optional'][package] = {'status': 'NOT_AVAILABLE', 'error': error}
    
    def check_version_constraints(self):
        """Check if installed versions meet requirements.txt constraints"""
        self.print_header("VERSION CONSTRAINTS CHECK")
        
        # Use relative path from script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_file = os.path.join(script_dir, 'requirements.txt')
        
        if not os.path.exists(requirements_file):
            print("⚠️  requirements.txt not found")
            return
        
        conflicts = []
        
        with open(requirements_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parse requirement
                if '==' in line:
                    package, required_version = line.split('==')
                    package = package.strip()
                    required_version = required_version.strip()
                    
                    try:
                        installed_version = pkg_resources.get_distribution(package).version
                        
                        if installed_version != required_version:
                            print(f"⚠️  {package}: required={required_version}, installed={installed_version}")
                            conflicts.append({
                                'package': package,
                                'required': required_version,
                                'installed': installed_version
                            })
                        else:
                            print(f"✅ {package}: {installed_version}")
                    except Exception as e:
                        print(f"❌ {package}: Not installed or error checking version")
                
                elif '>=' in line and '<' in line:
                    # Handle range requirements like numpy>=1.24.3,<2.0
                    parts = line.replace('>=', ' ').replace('<', ' ').replace(',', ' ').split()
                    if len(parts) >= 3:
                        package, min_ver, max_ver = parts[0], parts[1], parts[2]
                        try:
                            installed_version = pkg_resources.get_distribution(package).version
                            print(f"ℹ️  {package}: {min_ver} <= {installed_version} < {max_ver}")
                        except:
                            print(f"❌ {package}: Not installed")
        
        self.results['conflicts'] = conflicts
    
    def check_deprecated_features(self):
        """Check for deprecated features in libraries"""
        self.print_header("DEPRECATED FEATURES CHECK")
        
        # Test for known deprecated features
        deprecations = []
        
        # Check NumPy
        try:
            import numpy as np
            if hasattr(np, 'int'):
                # np.int is deprecated in NumPy 1.20+
                print("⚠️  NumPy: np.int is deprecated, use np.int_ or int instead")
                deprecations.append("NumPy: np.int is deprecated")
        except:
            pass
        
        # Check Pandas
        try:
            import pandas as pd
            version = pkg_resources.get_distribution('pandas').version
            major_version = int(version.split('.')[0])
            if major_version >= 2:
                print("ℹ️  Pandas 2.x: Some deprecated methods from 1.x may not work")
        except:
            pass
        
        # Check TensorFlow
        try:
            import tensorflow as tf
            version = pkg_resources.get_distribution('tensorflow').version
            major_version = int(version.split('.')[0])
            if major_version >= 2:
                print("ℹ️  TensorFlow 2.x: Using Keras integrated (tf.keras)")
        except:
            pass
        
        # Check Pillow
        try:
            from PIL import Image
            # In Pillow 10.0+, ANTIALIAS was removed (it was deprecated in earlier versions)
            if hasattr(Image, 'ANTIALIAS'):
                print("ℹ️  Pillow: Image.ANTIALIAS is available but deprecated, use Image.LANCZOS instead")
                deprecations.append("Pillow: Image.ANTIALIAS deprecated")
            else:
                print("ℹ️  Pillow: Image.ANTIALIAS removed (expected in Pillow 10+), use Image.LANCZOS")
        except:
            pass
        
        if not deprecations:
            print("✅ No critical deprecated features detected")
        
        self.results['deprecations'] = deprecations
    
    def test_module_functionality(self):
        """Test basic functionality of key modules"""
        self.print_header("MODULE FUNCTIONALITY TEST")
        
        tests_passed = 0
        tests_total = 0
        
        # Test NumPy
        tests_total += 1
        try:
            import numpy as np
            arr = np.array([1, 2, 3])
            assert arr.sum() == 6
            print("✅ NumPy: Basic array operations work")
            tests_passed += 1
        except Exception as e:
            print(f"❌ NumPy: {e}")
        
        # Test Pandas
        tests_total += 1
        try:
            import pandas as pd
            df = pd.DataFrame({'a': [1, 2, 3]})
            assert len(df) == 3
            print("✅ Pandas: Basic DataFrame operations work")
            tests_passed += 1
        except Exception as e:
            print(f"❌ Pandas: {e}")
        
        # Test Pillow
        tests_total += 1
        try:
            from PIL import Image
            import io
            # Create a simple image
            img = Image.new('RGB', (100, 100), color='red')
            assert img.size == (100, 100)
            print("✅ Pillow: Image creation and manipulation work")
            tests_passed += 1
        except Exception as e:
            print(f"❌ Pillow: {e}")
        
        # Test OpenCV
        tests_total += 1
        try:
            import cv2
            import numpy as np
            # Create a simple image
            img = np.zeros((100, 100, 3), dtype=np.uint8)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            assert gray.shape == (100, 100)
            print("✅ OpenCV: Image processing works")
            tests_passed += 1
        except Exception as e:
            print(f"❌ OpenCV: {e}")
        
        # Test Plotly
        tests_total += 1
        try:
            import plotly.graph_objects as go
            fig = go.Figure(data=[go.Bar(x=[1, 2, 3], y=[1, 2, 3])])
            assert fig is not None
            print("✅ Plotly: Chart creation works")
            tests_passed += 1
        except Exception as e:
            print(f"❌ Plotly: {e}")
        
        print(f"\n📊 Functionality Tests: {tests_passed}/{tests_total} passed")
        
        return tests_passed == tests_total
    
    def test_face_recognition_functionality(self):
        """Test face recognition functionality if available"""
        self.print_header("FACE RECOGNITION FUNCTIONALITY TEST")
        
        try:
            import face_recognition
            import numpy as np
            from PIL import Image
            
            # Create a dummy image
            img = Image.new('RGB', (100, 100), color='white')
            img_array = np.array(img)
            
            # Try face detection
            face_locations = face_recognition.face_locations(img_array)
            print("✅ face_recognition: Library loads and basic functions work")
            print(f"   (No faces detected in test image, which is expected)")
            
            return True
            
        except ImportError:
            print("⚠️  face_recognition: Not available (optional)")
            return False
        except Exception as e:
            print(f"❌ face_recognition: Error during functionality test: {e}")
            return False
    
    def generate_recommendations(self):
        """Generate recommendations based on test results"""
        self.print_header("RECOMMENDATIONS")
        
        recommendations = []
        
        # Check for failed basic libraries
        failed_basic = [pkg for pkg, info in self.results['basic'].items() 
                       if info['status'] == 'FAILED']
        
        if failed_basic:
            recommendations.append({
                'severity': 'CRITICAL',
                'issue': f"Basic libraries failed: {', '.join(failed_basic)}",
                'solution': "Run: pip install -r requirements.txt"
            })
        
        # Check for version conflicts
        if self.results['conflicts']:
            recommendations.append({
                'severity': 'WARNING',
                'issue': "Version conflicts detected",
                'solution': "Run: pip install -r requirements.txt --force-reinstall"
            })
        
        # Check for unavailable optional libraries
        unavailable_optional = [pkg for pkg, info in self.results['optional'].items() 
                               if info['status'] == 'NOT_AVAILABLE']
        
        if unavailable_optional:
            if 'dlib' in unavailable_optional or 'face-recognition' in unavailable_optional:
                recommendations.append({
                    'severity': 'INFO',
                    'issue': "Face recognition libraries not available",
                    'solution': (
                        "Optional: To enable face recognition:\n"
                        "   1. Install system dependencies (see packages.txt)\n"
                        "   2. For Ubuntu/Debian: sudo apt-get install build-essential cmake libopenblas-dev liblapack-dev\n"
                        "   3. For conda: conda install -c conda-forge dlib\n"
                        "   4. Then: pip install face-recognition\n"
                        "   See FACE_RECOGNITION_INSTALLATION.md for details"
                    )
                })
        
        # Check for deprecations
        if self.results['deprecations']:
            recommendations.append({
                'severity': 'INFO',
                'issue': f"Deprecated features detected: {len(self.results['deprecations'])}",
                'solution': "Review code for deprecated API usage and update as needed"
            })
        
        # Python version warnings
        if self.python_version >= (3, 12):
            recommendations.append({
                'severity': 'WARNING',
                'issue': "Python 3.12+ may have compatibility issues with some libraries",
                'solution': (
                    "Consider using Python 3.8-3.11 for production.\n"
                    "   Alternative: Use pyenv or conda to manage Python versions"
                )
            })
        
        # Print recommendations
        if not recommendations:
            print("✅ No critical issues found! All libraries are compatible.")
        else:
            for i, rec in enumerate(recommendations, 1):
                severity_symbol = {
                    'CRITICAL': '🔴',
                    'WARNING': '⚠️ ',
                    'INFO': 'ℹ️ '
                }.get(rec['severity'], 'ℹ️')
                
                print(f"\n{severity_symbol} {rec['severity']} #{i}:")
                print(f"   Issue: {rec['issue']}")
                print(f"   Solution: {rec['solution']}")
        
        self.results['recommendations'] = recommendations
        
        return recommendations
    
    def save_report(self, filename: str = 'compatibility_report.txt'):
        """Save detailed compatibility report to file"""
        # Use current working directory
        report_path = os.path.join(os.getcwd(), filename)
        
        with open(report_path, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("  LIBRARY COMPATIBILITY TEST REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Date: {subprocess.check_output(['date']).decode().strip()}\n")
            f.write(f"Python: {sys.version}\n\n")
            
            # Basic libraries
            f.write("BASIC LIBRARIES:\n")
            f.write("-" * 70 + "\n")
            for pkg, info in self.results['basic'].items():
                status = '✅' if info['status'] == 'OK' else '❌'
                version = info.get('version', 'unknown')
                f.write(f"{status} {pkg:<30} v{version}\n")
            f.write("\n")
            
            # Optional libraries
            f.write("OPTIONAL LIBRARIES:\n")
            f.write("-" * 70 + "\n")
            for pkg, info in self.results['optional'].items():
                status = '✅' if info['status'] == 'OK' else '⚠️'
                version = info.get('version', 'N/A')
                f.write(f"{status} {pkg:<30} v{version}\n")
            f.write("\n")
            
            # Conflicts
            if self.results['conflicts']:
                f.write("VERSION CONFLICTS:\n")
                f.write("-" * 70 + "\n")
                for conflict in self.results['conflicts']:
                    f.write(f"⚠️  {conflict['package']}: ")
                    f.write(f"required={conflict['required']}, ")
                    f.write(f"installed={conflict['installed']}\n")
                f.write("\n")
            
            # Deprecations
            if self.results['deprecations']:
                f.write("DEPRECATED FEATURES:\n")
                f.write("-" * 70 + "\n")
                for dep in self.results['deprecations']:
                    f.write(f"⚠️  {dep}\n")
                f.write("\n")
            
            # Recommendations
            if self.results['recommendations']:
                f.write("RECOMMENDATIONS:\n")
                f.write("-" * 70 + "\n")
                for i, rec in enumerate(self.results['recommendations'], 1):
                    f.write(f"\n{rec['severity']} #{i}:\n")
                    f.write(f"   Issue: {rec['issue']}\n")
                    f.write(f"   Solution: {rec['solution']}\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 70 + "\n")
        
        print(f"\n📝 Detailed report saved to: {report_path}")
    
    def run_all_tests(self):
        """Run all compatibility tests"""
        print("\n" + "=" * 70)
        print("  🔍 COMPREHENSIVE LIBRARY COMPATIBILITY TEST")
        print("=" * 70)
        
        # 1. Check Python version
        if not self.check_python_version():
            return False
        
        # 2. Test basic libraries
        basic_ok = self.test_basic_libraries()
        
        # 3. Test optional libraries
        self.test_optional_libraries()
        
        # 4. Check version constraints
        self.check_version_constraints()
        
        # 5. Check for deprecated features
        self.check_deprecated_features()
        
        # 6. Test module functionality
        functionality_ok = self.test_module_functionality()
        
        # 7. Test face recognition if available
        self.test_face_recognition_functionality()
        
        # 8. Generate recommendations
        recommendations = self.generate_recommendations()
        
        # 9. Save report
        self.save_report()
        
        # Final summary
        self.print_header("FINAL SUMMARY")
        
        critical_issues = any(r['severity'] == 'CRITICAL' for r in recommendations)
        
        if critical_issues:
            print("❌ CRITICAL ISSUES FOUND - System may not work properly")
            print("   Review recommendations above and apply fixes")
            return False
        elif not basic_ok or not functionality_ok:
            print("⚠️  WARNINGS FOUND - System should work but some features may be limited")
            print("   Review recommendations above for optimal performance")
            return True
        else:
            print("✅ ALL TESTS PASSED - System is ready to use!")
            print("   All libraries are compatible and working correctly")
            return True


def main():
    """Main function"""
    tester = CompatibilityTester()
    success = tester.run_all_tests()
    
    print("\n" + "=" * 70)
    print("  Test completed. Run 'streamlit run app.py' to start the application.")
    print("=" * 70 + "\n")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
