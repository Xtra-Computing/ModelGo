# ModelGo License Version 2.0

This directory contains the ModelGo License (MGL) Version 2.0 family, a modular licensing framework designed specifically for AI models.

## 📁 Directory Structure

```
V2/
├── README.md              # This file
├── ModelSheet.txt         # Comparison table of all licenses
├── MG0/                   # Most permissive license
│   └── LICENSE
├── MG-BY/                 # Attribution
│   └── LICENSE
├── MG-BY-NC/              # Attribution + NonCommercial
│   └── LICENSE
├── MG-BY-ND/              # Attribution + NoDerivatives
│   └── LICENSE
├── MG-BY-NC-ND/           # Attribution + NonCommercial + NoDerivatives
│   └── LICENSE
├── MG-BY-SA/              # Attribution + ShareAlike
│   └── LICENSE
├── MG-BY-RAI/             # Attribution + Responsible AI
│   └── LICENSE
└── MG-BY-NC-RAI/          # Attribution + NonCommercial + Responsible AI
    └── LICENSE
```

## 🎯 Quick Guide

### License Options

| License | Commercial Use | Derivatives | Distribution | RAI Restrictions |
|---------|----------------|-------------|--------------|------------------|
| **MG0** | ✓ | ✓ | ✓ | ✗ |
| **MG-BY** | ✓ | ✓ | ✓ | ✗ |
| **MG-BY-NC** | ✗ | ✓ | ✓ | ✗ |
| **MG-BY-ND** | ✓ | ✓ (private) | ✗ | ✗ |
| **MG-BY-NC-ND** | ✗ | ✓ (private) | ✗ | ✗ |
| **MG-BY-SA** | ✓ | ✓ | ✓ (same license) | ✗ |
| **MG-BY-RAI** | ✓ | ✓ | ✓ | ✓ |
| **MG-BY-NC-RAI** | ✗ | ✓ | ✓ | ✓ |

### Module Meanings

- **BY** (Attribution): Require attribution when distributing
- **NC** (NonCommercial): Restrict to non-commercial use only
- **ND** (NoDerivatives): Allow creation but prohibit distribution of derivatives
- **SA** (ShareAlike): Require derivatives to use the same license
- **RAI** (Responsible AI): Include 14 use restrictions for ethical AI deployment

## 📋 Model Sheet

For a detailed comparison of all licenses, see [`ModelSheet.txt`](./ModelSheet.txt).

The Model Sheet provides a comprehensive view of:
- Grant of rights for each license
- Requirements for distribution
- Restrictions and conditions

## 🆕 What's New in V2.0

### Key Updates (December 2025)

1. **Extracted Models Support**
   - Added explicit definitions and rights for models created through distillation
   - Clear distribution rules for extracted models

2. **Enhanced NoDerivatives Licenses**
   - Explicit prohibition: "You do not have permission to Distribute any Derivative Materials or Extracted Models"
   - Allows private creation and use of derivatives

3. **Improved Clarity**
   - Updated all licenses to cover Licensed Materials, Derivative Materials, and Extracted Models
   - Consistent terminology across all license variants

## 💡 How to Choose

- **MG0**: Share your model freely without any conditions
- **MG-BY**: Require attribution only
- **MG-BY-NC**: For non-commercial projects (research, education)
- **MG-BY-ND**: Allow use but prevent redistribution of modified versions
- **MG-BY-SA**: Ensure derivatives remain open under the same terms
- **MG-BY-RAI**: Add ethical use restrictions (14 prohibited uses)
- **MG-BY-NC-RAI**: Combine non-commercial and ethical restrictions

For detailed guidance, visit [modelgo.li/get-started/how-to-choose](https://www.modelgo.li/get-started/how-to-choose)

## 📖 Resources

- **Website**: [modelgo.li](https://www.modelgo.li)
- **Documentation**: [modelgo.li/docs](https://www.modelgo.li/docs)
- **GitHub**: [github.com/Xtra-Computing/ModelGo](https://github.com/Xtra-Computing/ModelGo)

## 📄 License

ModelGo License © 2025 National University of Singapore

---

**Version**: 2.0  
**Release Date**: December 2025  
**Status**: Stable
