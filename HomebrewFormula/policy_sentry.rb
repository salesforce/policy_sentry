class PolicySentry < Formula
  include Language::Python::Virtualenv

  desc "Shiny new formula"
  homepage "https://github.com/salesforce/policy_sentry"
  url "https://files.pythonhosted.org/packages/69/08/19f2f761da39b93ab6bb736cc6c05cce64448afac0d14c5d6391e6022769/policy_sentry-0.12.3.tar.gz"
  sha256 "75137fc7e1311bc24836855dce7caa40548f3f81a72045bb6731d55f48de644a"

  depends_on "python3"

  resource "beautifulsoup4" do
    url "https://files.pythonhosted.org/packages/e8/b0/cd2b968000577ec5ce6c741a54d846dfa402372369b8b6861720aa9ecea7/beautifulsoup4-4.11.1.tar.gz"
    sha256 "ad9aa55b65ef2808eb405f46cf74df7fcb7044d5cbc26487f96eb2ef2e436693"
  end

  resource "certifi" do
    url "https://files.pythonhosted.org/packages/6c/ae/d26450834f0acc9e3d1f74508da6df1551ceab6c2ce0766a593362d6d57f/certifi-2021.10.8.tar.gz"
    sha256 "78884e7c1d4b00ce3cea67b44566851c4343c120abd683433ce934a68ea58872"
  end

  resource "charset-normalizer" do
    url "https://files.pythonhosted.org/packages/56/31/7bcaf657fafb3c6db8c787a865434290b726653c912085fbd371e9b92e1c/charset-normalizer-2.0.12.tar.gz"
    sha256 "2857e29ff0d34db842cd7ca3230549d1a697f96ee6d3fb071cfa6c7393832597"
  end

  resource "click" do
    url "https://files.pythonhosted.org/packages/42/e1/4cb2d3a2416bcd871ac93f12b5616f7755a6800bccae05e5a99d3673eb69/click-8.1.2.tar.gz"
    sha256 "479707fe14d9ec9a0757618b7a100a0ae4c4e236fac5b7f80ca68028141a1a72"
  end

  resource "contextlib2" do
    url "https://files.pythonhosted.org/packages/c7/13/37ea7805ae3057992e96ecb1cffa2fa35c2ef4498543b846f90dd2348d8f/contextlib2-21.6.0.tar.gz"
    sha256 "ab1e2bfe1d01d968e1b7e8d9023bc51ef3509bba217bb730cee3827e1ee82869"
  end

  resource "idna" do
    url "https://files.pythonhosted.org/packages/62/08/e3fc7c8161090f742f504f40b1bccbfc544d4a4e09eb774bf40aafce5436/idna-3.3.tar.gz"
    sha256 "9d643ff0a55b762d5cdb124b8eaa99c66322e2157b69160bc32796e824360e6d"
  end

  resource "importlib-metadata" do
    url "https://files.pythonhosted.org/packages/3e/1d/964b27278cfa369fbe9041f604ab09c6e99556f8b7910781b4584b428c2f/importlib_metadata-4.11.3.tar.gz"
    sha256 "ea4c597ebf37142f827b8f39299579e31685c31d3a438b59f469406afd0f2539"
  end

  resource "PyYAML" do
    url "https://files.pythonhosted.org/packages/36/2b/61d51a2c4f25ef062ae3f74576b01638bebad5e045f747ff12643df63844/PyYAML-6.0.tar.gz"
    sha256 "68fb519c14306fec9720a2a5b45bc9f0c8d1b9c72adf45c37baedfcd949c35a2"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/60/f3/26ff3767f099b73e0efa138a9998da67890793bfa475d8278f84a30fec77/requests-2.27.1.tar.gz"
    sha256 "68d7c56fd5a8999887728ef304a6d12edc7be74f1cfa47714fc8b414525c9a61"
  end

  resource "schema" do
    url "https://files.pythonhosted.org/packages/4e/e8/01e1b46d9e04cdaee91c9c736d9117304df53361a191144c8eccda7f0ee9/schema-0.7.5.tar.gz"
    sha256 "f06717112c61895cabc4707752b88716e8420a8819d71404501e114f91043197"
  end

  resource "soupsieve" do
    url "https://files.pythonhosted.org/packages/3b/3d/a7865440c393baf403899d79e724ad0a9805199962917745d9277f1db40e/soupsieve-2.3.2.tar.gz"
    sha256 "0bcc6d7432153063e3df09c3ac9442af3eba488715bfcad6a4c38ccb2a523124"
  end

  resource "typing-extensions" do
    url "https://files.pythonhosted.org/packages/b1/5a/8b5fbb891ef3f81fc923bf3cb4a578c0abf9471eb50ce0f51c74212182ab/typing_extensions-4.1.1.tar.gz"
    sha256 "1a9462dcc3347a79b1f1c0271fbe79e844580bb598bafa1ed208b94da3cdcd42"
  end

  resource "urllib3" do
    url "https://files.pythonhosted.org/packages/1b/a5/4eab74853625505725cefdf168f48661b2cd04e7843ab836f3f63abf81da/urllib3-1.26.9.tar.gz"
    sha256 "aabaf16477806a5e1dd19aa41f8c2b7950dd3c746362d7e3223dbe6de6ac448e"
  end

  resource "zipp" do
    url "https://files.pythonhosted.org/packages/cc/3c/3e8c69cd493297003da83f26ccf1faea5dd7da7892a0a7c965ac3bcba7bf/zipp-3.8.0.tar.gz"
    sha256 "56bf8aadb83c24db6c4b577e13de374ccfb67da2078beba1d037c17980bf43ad"
  end

  def install
    virtualenv_create(libexec, "python3")
    virtualenv_install_with_resources
  end

  test do
    false
  end
end
