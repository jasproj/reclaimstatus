import React, { useState } from 'react';

const STATES = [
  'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
  'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
  'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
  'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
  'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
  'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
  'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
  'Wisconsin', 'Wyoming'
];

const TreasuryPackageForm = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({
    firstName: '',
    middleName: '',
    lastName: '',
    ssn: '',
    birthDate: '',
    birthState: '',
    birthCertNumber: '',
    streetAddress: '',
    city: '',
    county: '',
    state: '',
    zipCode: '',
    uccFilingNumber: '',
    uccFilingState: 'New York',
    registeredMailNumber: '',
    dtcRoutingNumber: '',
    dtcAccountNumber: '',
    documentDate: new Date().toISOString().split('T')[0],
    lienAmount: '100000000'
  });
  const [errors, setErrors] = useState({});
  const [isGenerating, setIsGenerating] = useState(false);

  const steps = [
    { id: 'personal', title: 'Personal Information', icon: '👤' },
    { id: 'address', title: 'Address', icon: '🏠' },
    { id: 'ucc', title: 'UCC Filing', icon: '📋' },
    { id: 'financial', title: 'Financial', icon: '💰' },
    { id: 'review', title: 'Review & Generate', icon: '✅' }
  ];

  // Derived fields
  const getDerivedFields = () => {
    const fullNameUpper = `${formData.firstName} ${formData.middleName} ${formData.lastName}`.toUpperCase().replace(/\s+/g, ' ').trim();
    const fullNameStyled = `${formData.firstName}-${formData.middleName}: ${formData.lastName}`;
    const ssnNoDashes = formData.ssn.replace(/-/g, '');
    
    return {
      fullNameUpper,
      fullNameStyled,
      ssnNoDashes,
      streetAddressUpper: formData.streetAddress.toUpperCase(),
      cityUpper: formData.city.toUpperCase(),
      stateUpper: formData.state.toUpperCase(),
      countyUpper: formData.county.toUpperCase()
    };
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  const formatSSN = (value) => {
    const digits = value.replace(/\D/g, '').slice(0, 9);
    if (digits.length >= 6) return `${digits.slice(0,3)}-${digits.slice(3,5)}-${digits.slice(5)}`;
    if (digits.length >= 4) return `${digits.slice(0,3)}-${digits.slice(3)}`;
    return digits;
  };

  const validateStep = (stepIndex) => {
    const newErrors = {};
    
    if (stepIndex === 0) {
      if (!formData.firstName.trim()) newErrors.firstName = 'Required';
      if (!formData.lastName.trim()) newErrors.lastName = 'Required';
      if (!formData.ssn || formData.ssn.replace(/-/g, '').length !== 9) newErrors.ssn = 'Valid SSN required';
      if (!formData.birthDate) newErrors.birthDate = 'Required';
      if (!formData.birthState) newErrors.birthState = 'Required';
      if (!formData.birthCertNumber.trim()) newErrors.birthCertNumber = 'Required';
    }
    
    if (stepIndex === 1) {
      if (!formData.streetAddress.trim()) newErrors.streetAddress = 'Required';
      if (!formData.city.trim()) newErrors.city = 'Required';
      if (!formData.county.trim()) newErrors.county = 'Required';
      if (!formData.state) newErrors.state = 'Required';
      if (!formData.zipCode || !/^\d{5}(-\d{4})?$/.test(formData.zipCode)) newErrors.zipCode = 'Valid ZIP required';
    }
    
    if (stepIndex === 2) {
      if (!formData.uccFilingNumber.trim()) newErrors.uccFilingNumber = 'Required';
      if (!formData.registeredMailNumber.trim()) newErrors.registeredMailNumber = 'Required';
    }
    
    if (stepIndex === 3) {
      if (!formData.dtcRoutingNumber.trim()) newErrors.dtcRoutingNumber = 'Required';
      if (!formData.dtcAccountNumber.trim()) newErrors.dtcAccountNumber = 'Required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const nextStep = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => Math.min(prev + 1, steps.length - 1));
    }
  };

  const prevStep = () => {
    setCurrentStep(prev => Math.max(prev - 1, 0));
  };

  const generatePackage = async () => {
    setIsGenerating(true);
    const derived = getDerivedFields();
    const payload = { ...formData, ...derived };
    
    try {
      const response = await fetch('/api/generate-package', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Treasury_Package_${formData.lastName}_${formData.documentDate}.zip`;
        a.click();
      } else {
        alert('Error generating package. Please try again.');
      }
    } catch (error) {
      console.error('Generation error:', error);
      alert('Error generating package. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const InputField = ({ label, field, type = 'text', placeholder, required = true, help }) => (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      <input
        type={type}
        value={formData[field]}
        onChange={(e) => handleChange(field, e.target.value)}
        placeholder={placeholder}
        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
          errors[field] ? 'border-red-500' : 'border-gray-300'
        }`}
      />
      {errors[field] && <p className="text-red-500 text-xs mt-1">{errors[field]}</p>}
      {help && <p className="text-gray-500 text-xs mt-1">{help}</p>}
    </div>
  );

  const SelectField = ({ label, field, options, required = true }) => (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      <select
        value={formData[field]}
        onChange={(e) => handleChange(field, e.target.value)}
        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 ${
          errors[field] ? 'border-red-500' : 'border-gray-300'
        }`}
      >
        <option value="">Select...</option>
        {options.map(opt => <option key={opt} value={opt}>{opt}</option>)}
      </select>
      {errors[field] && <p className="text-red-500 text-xs mt-1">{errors[field]}</p>}
    </div>
  );

  const renderStep = () => {
    switch (currentStep) {
      case 0:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold mb-4">Personal Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <InputField label="First Name" field="firstName" placeholder="Thomas" />
              <InputField label="Middle Name" field="middleName" placeholder="Kallen" required={false} />
              <InputField label="Last Name" field="lastName" placeholder="Claycomb" />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Social Security Number <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={formData.ssn}
                onChange={(e) => handleChange('ssn', formatSSN(e.target.value))}
                placeholder="XXX-XX-XXXX"
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 ${
                  errors.ssn ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.ssn && <p className="text-red-500 text-xs mt-1">{errors.ssn}</p>}
              <p className="text-gray-500 text-xs mt-1">🔒 Encrypted in transit and at rest</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InputField label="Date of Birth" field="birthDate" type="date" />
              <SelectField label="State of Birth" field="birthState" options={STATES} />
            </div>
            <InputField 
              label="Birth Certificate Number" 
              field="birthCertNumber" 
              placeholder="XXX-XX-XXXXXX"
              help="Found on your birth certificate (varies by state)"
            />
          </div>
        );
      
      case 1:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold mb-4">Address Information</h3>
            <InputField label="Street Address" field="streetAddress" placeholder="6316 East 113th Avenue" />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InputField label="City" field="city" placeholder="Temple Terrace" />
              <InputField label="County" field="county" placeholder="Hillsborough" />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <SelectField label="State" field="state" options={STATES} />
              <InputField label="ZIP Code" field="zipCode" placeholder="33617" />
            </div>
          </div>
        );
      
      case 2:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold mb-4">UCC Filing Information</h3>
            <InputField 
              label="UCC-1 Filing Number" 
              field="uccFilingNumber" 
              placeholder="Enter your UCC filing number"
              help="From your Secretary of State UCC filing"
            />
            <SelectField label="UCC Filing State" field="uccFilingState" options={STATES} />
            <InputField 
              label="Registered Mail Tracking Number" 
              field="registeredMailNumber" 
              placeholder="RF737860948US"
              help="USPS Registered Mail number for Treasury package"
            />
          </div>
        );
      
      case 3:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold mb-4">Financial Routing</h3>
            <InputField 
              label="DTC Routing Number" 
              field="dtcRoutingNumber" 
              placeholder="0810-0004-5"
            />
            <InputField 
              label="DTC Account Number" 
              field="dtcAccountNumber" 
              placeholder="053045139"
            />
            <InputField 
              label="Document Execution Date" 
              field="documentDate" 
              type="date"
            />
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Lien Amount
              </label>
              <div className="flex items-center">
                <span className="text-gray-500 mr-2">$</span>
                <input
                  type="text"
                  value={Number(formData.lienAmount).toLocaleString()}
                  onChange={(e) => handleChange('lienAmount', e.target.value.replace(/[^\d]/g, ''))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <p className="text-gray-500 text-xs mt-1">Default: $100,000,000.00</p>
            </div>
          </div>
        );
      
      case 4:
        const derived = getDerivedFields();
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold mb-4">Review Your Information</h3>
            
            <div className="bg-gray-50 rounded-lg p-4 space-y-3">
              <h4 className="font-medium text-gray-900">Name Formats</h4>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <span className="text-gray-600">ALL CAPS:</span>
                <span className="font-mono">{derived.fullNameUpper}</span>
                <span className="text-gray-600">Styled:</span>
                <span className="font-mono">{derived.fullNameStyled}</span>
              </div>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4 space-y-3">
              <h4 className="font-medium text-gray-900">Personal Details</h4>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <span className="text-gray-600">SSN:</span>
                <span className="font-mono">***-**-{formData.ssn.slice(-4)}</span>
                <span className="text-gray-600">Birth Date:</span>
                <span>{formData.birthDate}</span>
                <span className="text-gray-600">Birth State:</span>
                <span>{formData.birthState}</span>
              </div>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4 space-y-3">
              <h4 className="font-medium text-gray-900">Address</h4>
              <p className="text-sm">
                {formData.streetAddress}<br />
                {formData.city}, {formData.state} {formData.zipCode}<br />
                {formData.county} County
              </p>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4 space-y-3">
              <h4 className="font-medium text-gray-900">Filing Information</h4>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <span className="text-gray-600">UCC Filing:</span>
                <span className="font-mono">{formData.uccFilingNumber}</span>
                <span className="text-gray-600">Registered Mail:</span>
                <span className="font-mono">{formData.registeredMailNumber}</span>
              </div>
            </div>
            
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-medium text-blue-900 mb-2">📦 Package Contents</h4>
              <p className="text-sm text-blue-800">
                Your Treasury Package will include 21 documents, fully populated with your information,
                ready for notarization and mailing to the Department of Treasury.
              </p>
            </div>
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Treasury Package Generator</h1>
          <p className="text-slate-400">Complete the questionnaire to generate your document package</p>
        </div>
        
        {/* Progress Steps */}
        <div className="flex justify-between mb-8">
          {steps.map((step, index) => (
            <div 
              key={step.id}
              className={`flex flex-col items-center ${index <= currentStep ? 'text-blue-400' : 'text-slate-600'}`}
            >
              <div className={`w-10 h-10 rounded-full flex items-center justify-center text-lg mb-1 ${
                index < currentStep ? 'bg-blue-600 text-white' :
                index === currentStep ? 'bg-blue-500 text-white' : 'bg-slate-700'
              }`}>
                {index < currentStep ? '✓' : step.icon}
              </div>
              <span className="text-xs hidden md:block">{step.title}</span>
            </div>
          ))}
        </div>
        
        {/* Form Card */}
        <div className="bg-white rounded-xl shadow-2xl p-6 md:p-8">
          {renderStep()}
          
          {/* Navigation */}
          <div className="flex justify-between mt-8 pt-6 border-t">
            <button
              onClick={prevStep}
              disabled={currentStep === 0}
              className={`px-6 py-2 rounded-lg font-medium ${
                currentStep === 0 
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              ← Back
            </button>
            
            {currentStep < steps.length - 1 ? (
              <button
                onClick={nextStep}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700"
              >
                Continue →
              </button>
            ) : (
              <button
                onClick={generatePackage}
                disabled={isGenerating}
                className={`px-8 py-3 rounded-lg font-medium ${
                  isGenerating 
                    ? 'bg-gray-400 cursor-wait'
                    : 'bg-green-600 hover:bg-green-700 text-white'
                }`}
              >
                {isGenerating ? '⏳ Generating...' : '📥 Generate Package'}
              </button>
            )}
          </div>
        </div>
        
        {/* Security Notice */}
        <div className="mt-6 text-center text-slate-500 text-sm">
          🔒 Your data is encrypted and never stored on our servers
        </div>
      </div>
    </div>
  );
};

export default TreasuryPackageForm;
