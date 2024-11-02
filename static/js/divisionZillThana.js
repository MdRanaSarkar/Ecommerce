// Division Section select
function divisionsList() {
  console.log($("#select-division-input-3").val());
  // Define a mapping of divisions to their respective districts
  const divisionDistricts = {
      Barishal: ['Barguna', 'Barishal', 'Bhola', 'Jhalokhathi', 'Patuakhali', 'Pirojpur'],
      Chattogram: ['Bandarban', 'Chandpur', 'Chattogram', 'Cumilla', 'Cox\'s Bazar', 'Feni', 'Khagrachhari', 'Noakhali', 'Rangamati', 'Lakshmipur'],
      Dhaka: ['Dhaka', 'Faridpur', 'Gazipur', 'Gopalganj', 'Kishoreganj', 'Madaripur', 'Manikganj', 'Munshiganj', 'Narayanganj', 'Narsingdi', 'Rajbari', 'Shariatpur', 'Tangail'],
      Khulna: ['Bagerhat', 'Chuadanga', 'Jashore', 'Jhenaidah', 'Khulna', 'Kushtia', 'Magura', 'Meharpur', 'Narail', 'Satkhira'],
      Mymensingh: ['Jamalpur', 'Mymensingh', 'Netrokona', 'Sherpur'],
      Rajshahi: ['Bogura', 'ChapaiNawabganj', 'Jaipurhat', 'Naogaon', 'Natore', 'Pabna', 'Rajshahi', 'Sirajganj'],
      Rangpur: ['Dinajpur', 'Gaibandha', 'Lalmonirhat', 'Nilphamari', 'Panchagarh', 'Rangpur', 'Thakurgaon'],
      Sylhet: ['Habiganj', 'Mauluvibazar', 'Sunamganj', 'Sylhet']
  };

  // Get selected division
  var diviList = $("#select-division-input-3").val();
  // Get the district list based on the selected division
  let disctList = '<option disabled selected>Select District</option>';
  if (divisionDistricts[diviList]) {
      divisionDistricts[diviList].forEach(district => {
          disctList += `<option value="${district}">${district}</option>`;
      });
  }

  console.log(disctList)

  // Update the district dropdown
  document.getElementById("distr").innerHTML= disctList;
  document.getElementById("selectCityData").innerHTML= disctList;
}

function thanaList() {
  var distric_data = {
      Bagerhat: ['Bagerhat Sadar', 'Chitalmari', 'Fakirhat', 'Kachua', 'Mollahat', 'Mongla', 'Morrelganj', 'Rampal', 'Sarankhola', 'Others'],
      'Bandarban': ['Alikadam', 'Bandarban Sadar', 'Lama', 'Naikhongchhari', 'Rowangchhari', 'Ruma', 'Thanchi', 'Others'],
      Barguna: ['Amtali', 'Bamna', 'Barguna Sadar', 'Betagi', 'Patharghata', 'Others'],
      Barishal: ['Agailjhara', 'Babuganj', 'Bakerganj', 'Banari Para', 'Barishal Sadar (Kotwali)', 'Gaurnadi', 'Hizla', 'Mehendiganj', 'Muladi', 'Wazirpur', 'Others'],
       Bhola: ['Bhola Sadar', 'Burhanuddin', 'Char Fasson', 'Daulatkhan', 'Lalmohan', 'Manpura', 'Tazumuddin', 'Others'],
       Bogura: ['Adamdighi', 'Bogura Sadar', 'Dhunat', 'Dhupchanchia', 'Gabtali', 'Kahaloo', 'Nandigram', 'Sariakandi', 'Shajhanpur', 'Sherpur', 'Shibganj', 'Sonatola', 'Others'],
       Brahmanbaria: ['Akhaura', 'Ashuganj', 'Banchharampur', 'Bijoynagar', 'Brahmanbaria Sadar', 'Kasba', 'Nabinagar', 'Nasirnagar', 'Sarail', 'Others'],
       Chandpur: ['Chandpur Sadar', 'Faridganj', 'Haim Char', 'Hajiganj', 'Kachua', 'Matlab', 'Shahrasti', 'Uttar Matlab', 'Others'],
       ChapaiNawabganj: ['Bholahat', 'Gomastapur', 'Nachole', 'Nawabganj Sadar', 'Shibganj', 'Others'],
       Chattogram: ['Akbar Shah', 'Anowara', 'Bakalia', 'Bandar(Chitt. Port)', 'Banshkhali', 'Bayejid Bostami', 'Boalkhali', 'Chandanish', 'Chandgaon', 'Chawkbazar', 'Double Mooring', 'EPZ', 'Fatikchhari', 'Halishahar', 'Hathazari', 'Karnafuli', 'Khulshi', 'Kotwali', 'Lohagara', 'Mirsharai', 'Pahartali', 'Panchlaish', 'Patenga', 'Patiya', 'Rangunia', 'Raozan', 'Sadarghat', 'Sandwip', 'Satkania', 'Sitakunda', 'Others'],
       Chuadanga: ['Alamdanga', 'Chuadanga Sadar', 'Damurhuda', 'Jiban Nagar', 'Others'],
      'Cox\'s Bazar': ['Chakaria', 'Cox\'s Bazar Sadar', 'Kutubdia', 'Maheshkhali', 'Pekua', 'Ramu', 'Teknaf', 'Ukhia', 'Others'],
      Cumilla: ['Barura', 'Brahaman Para', 'Burichang', 'Chandina', 'Chauddagram', 'Cumilla Sadar', 'Cumilla Sadar South', 'Daudkandi', 'Debidwar', 'Homna', 'Laksam', 'Langalkot', 'Meghna', 'Monohorganj', 'Muradnagar', 'Titas', 'Others'],
       Dhaka: ['Adabor', 'Airport', 'Badda', 'Banani', 'Bangshal', 'Bhashantek', 'Cantonment', 'Chackbazar', 'Dakshin Khan', 'Darus-Salam', 'Demra', 'Dhamrai', 'Dhanmondi', 'Dohar', 'Gandaria', 'Gulshan', 'Hatirjheel', 'Hazaribhag', 'Jattrabari', 'Kadamtoli', 'Kafrul', 'Kalabagan', 'Kamrangir Char', 'Keraniganj Model', 'Khilgaon', 'Khilkhet', 'Kotwali', 'Lalbag', 'Mirpur Model', 'Mohammadpur', 'Motijheel', 'Mugda', 'Nawabganj', 'New Market', 'Pallabi', 'Paltan Model', 'Ramna Model', 'Rampura', 'Rupnagar', 'Sabujbhag', 'Savar', 'Shah Ali', 'Shahbag', 'Shahjahanpur', 'Sher e Bangla Nagar', 'Shyampur', 'South Keraniganj', 'Sutrapur', 'Tejgaon', 'Tejgaon Industrial', 'Turag', 'Uttar Khan', 'Uttara East', 'Uttara West', 'Vatara', 'Wari', 'Others'],
       Dinajpur: ['Biral', 'Birampur', 'Birganj', 'Bochaganj', 'Chirirbandar', 'Dinajpur Sadar', 'Fulbari', 'Ghoraghat', 'Hakimpur', 'Kaharole', 'Khansama', 'Nawabganj', 'Parbatipur', 'Others'],
       Faridpur: ['Alfadanga', 'Bhanga', 'Boalmari', 'Char Bhadrasan', 'Faridpur Sadar', 'Madukhali', 'Nagarkanda', 'Sadarpur', 'Saltha', 'Others'],
       Feni: ['Chhagalnayian', 'Daganbhuyian', 'Feni Sadar', 'Fulgazi', 'Parshuram', 'Sonagazi', 'Others'],
       Gaibandha: ['Fulchhari', 'Gaibandha Sadar', 'Gobidaganj', 'Palashbari', 'Sadullapur', 'Saghatta', 'Sundarganj', 'Others'],
       Gazipur: ['Gazipur Sadar', 'Kaliakair', 'Kaliganj', 'Kapasia', 'Sreepur', 'Tongi', 'Others'],
       Gopalganj: [
        'Gopalganj Sadar', 'Kashiani', 'Kotalipara', 'Muksudpur', 'Tungi Para', 'Others'
        ],
        Habiganj: [
            'Ajmirganj', 'Bahubal', 'Baniachang', 'Chunarughat', 'Habiganj Sadar',
            'Lakhai', 'Madhabpur', 'Nabiganj', 'Shayestaganj', 'Others'
        ],
        Jaipurhat: [
            'Akkelpur', 'Joypurhat Sadar', 'Kalai', 'Khetlal', 'Panchbibi', 'Others'
        ],
        Jamalpur: [
            'Bakshiganj', 'Dewanganj', 'Islampur', 'Jamalpur Sadar',
            'Madarganj', 'Melandaha', 'Sarishabari', 'Others'
        ],
        Jashore: ["Abhay Nagar", "Bagherpara", "Chowghacha", "Jhikargacha", "Keshabpur", "Kotwali", "Manirampur", "Sharsha", "Others"],
        Jhalokhathi: ["Jhalokhathi Sadar", "Kanthalia", "Nalchity", "Rajapur", "Others"],
        Jhenaidah: ["Harinakunda", "Jhenaidah Sadar", "Kaliganj", "Kotchandpur", "Mahespur", "Shailkupa", "Others"],
        Khagrachhari: ["Dighinala", "Khagrachhari Sadar", "Lakshmichhari", "Mahalchhari", "Manikchhari", "Matiranga", "Panchhari", "Ramgarh", "Others"],
        Khulna: ["Batiaghata", "Dacope", "Daulatpur", "Dighala", "Dumuria", "Khalishpur", "Khan Jahan Ali", "Khulna Sadar", "Koyra", "Paikgachha", "Phultala", "Rupsa", "Sonadanga", "Terokhada", "Others"],
        Kishoreganj: ["Austagram", "Bajitpur", "Bhairab", "Hossenpur", "Itna", "Karimganj", "Katiadi", "Kishoregonj SADAR", "Kuliar Char", "Mithamoin", "Nikli", "Pakundia", "Tarail", "Others"],
        Kurigram: ["Bhurungamari", "Char Rajibpur", "Chilmari", "Kurigram Sadar", "Nageshwari", "Phulbari", "Rajarhat", "Rajibpur", "Rowmari", "Ulipur", "Others"],
        Kushtia: ["Bheramara", "Daulatpur", "Khoksa", "Kumarkhali", "Kushtia Sadar", "Mirpur", "Others"],
        Lalmonirhat: ["Aditmari", "Hatibanda", "Kaliganj", "Lalmonirhat Sadar", "Patgram", "Others"],
        Lakshmipur: ["Komol Nogor", "Lakshmipur Sadar", "Raipur", "Ramganj", "Ramgati", "Others"],
        Madaripur: ["Kalkini", "Madaripur Sadar", "Rajoir", "Shibchar", "Others"],
        Magura: ["Magura Sadar", "Mohammadpur", "Shalikha", "Sreepur", "Others"],
        Manikganj: ["Daulatpur", "Ghior", "Harirampur", "Manikganj Sadar", "Saturia", "Shibalaya", "Singair", "Others"],
        Meharpur: ["Gangni", "Meherpur Sadar", "Mujib Nagar", "Others"],
        Mauluvibazar: ["Barlekha", "Juri", "Kamalganj", "Kulaura", "Maulvi Bazar Sadar", "Rajnagar", "Sreemangal", "Others"],
        Munshiganj: ["Gazaria", "Louhajang", "Munshiganj Sadar", "Serajdikhan", "Sreenagar", "Tongibari", "Others"],
        Mymensingh: ["Bhalukha", "Dhobaura", "Fulbaria", "Gaffargaon", "Gauripur", "Haluaghat", "Ishwarganj", "Muktagachha", "Mymensingh Sadar", "Nandail", "Phulpur", "Tarakanda", "Trishal", "Others"],
        Naogaon: ["Atrai", "Badalgachhi", "Dhamoirhat", "Mahadebpur", "Manda", "Naogaon Sadar", "Niamatpur", "Patnitala", "Porsha", "Raninagar", "Sapahar", "Others"],
        Narail: ["Kalia", "Lohagara", "Narail Sadar", "Others"],
        Narayanganj: ["Araihazar", "Bandar", "Narayanganj Sadar", "Rupganj", "Siddirganj", "Sonargaon", "Others"],
        Narsingdi: ["Belabo", "Manohardi", "Narsingdi Sadar", "Palash", "Roypura", "Shibpur", "Others"],
        Natore: ["Bagati Para", "Baraigram", "Gurudaspur", "Lalpur", "Naldanga", "Natore Sadar", "Singra", "Others"],
        Netrokona: ["Atpara", "Barhatta", "Durgapur", "Kalmakanda", "Kendua", "Khaliajuri", "Madan", "Mohanganj", "Netrokona Sadar", "Purbadhala", "Others"],
        Nilphamari: ["Dimla", "Domar", "Jaldhaka", "Kishoreganj", "Nilphamari Sadar", "Saidpur", "Others"],
        Noakhali: ["Begumganj", "Chatkhil", "Companiganj", "Hatiya", "Kobirhat", "Noakhali Sadar (Sudharam)", "Senbagh", "Sonaimuri", "Others"],
        Pabna: ["Atgharia", "Bera", "Bhangura", "Chatmohar", "Faridpur", "Ishwardi", "Pabna Sadar", "Santhia", "Sujanagar", "Others"],
        Panchagarh: ["Atwari", "Boda", "Debiganj", "Panchagarh Sadar", "Tentulia", "Others"],
        Patuakhali: ["Bauphal", "Dashmina", "Dumki", "Galachipa", "Kala Para", "Mirzaganj", "Patuakhali Sadar", "Rangabali", "Others"],
        Pirojpur: ["Bhandaria", "Indurkani", "Kawkhali", "Mathbaria", "Nazirpur", "Nesarabad (Swarupkati)", "Pirojpur Sadar", "Others"],
        Rajbari: ["Balia Kandi", "Goalandaghat", "Kalukhali", "Pangsha", "Rajbari Sadar", "Others"],
        Rajshahi: ["Balia Kandi", "Goalandaghat", "Kalukhali", "Pangsha", "Rajbari Sadar", "Others"],
        Rangamati: ["Bagaichhari", "Barkal", "Belaichhari", "Juraichhari", "Kaptai", "Kawkhali (Betbunia)", "Langadu", "Naniarchar", "Rajasthali", "Rangamati Sadar", "Others"],
        Rangpur: ["Badarganj", "Gangachara", "Kaunia", "Mitha Pukur", "Pirgachha", "Pirganj", "Rangpur Sadar", "Taraganj", "Others"],
        Satkhira: ["Assasuni", "Debhata", "Kalaroa", "Kaliganj", "Satkhira Sadar", "Shyamnagar", "Tala", "Others"],
        Shariatpur: ["Bhaderganj", "Damudya", "Gosairhat", "Naria", "Palong(Sadar)", "Zanjira", "Others"],
        Sherpur: ["Jhenaigati", "Nakla", "Nalitabari", "Sherpur Sadar", "Sreebardi", "Others"],
        Sirajganj: ["Belkuchi", "Chauhali", "Kamarkhanda", "Kazipur", "Royganj", "Shahjadpur", "Sirajganj Sadar", "Tarash", "Ullah Para", "Others"],
        Sunamganj: ["Bishwambarpur", "Chhatak", "Daxin Sunamganj", "Derai", "Dharampasha", "Dowarabazar", "Jagannatpur", "Jamalganj", "Sulla", "Sunamganj Sadar", "Tahirpur", "Others"],
        Sylhet: ["Balaganj", "Beani Bazar", "Bishwanath", "Companiganj", "Fenchuganj", "Golabganj", "Gowainghat", "Jaintiapur", "Kanaighat", "Kowtali", "South Surma", "Zakirganj", "Others"],
        Tangail: ["Basail", "Bhuapur", "Delduar", "Dhonbari", "Ghatail", "Gopalpur", "Kalihati", "Madhupur", "Mirzapur", "Nagarpur", "Sakhipur", "Tangail Sadar", "Others"],
        Thakurgaon: ["Baliadangi", "Haripur", "Pirganj", "Ranisankail", "Thakurgaon Sadar", "Others"]

  };

  var DisList = document.getElementById('distr').value;
  var thanaOptions = '<option value="">Select One</option>';

  if (distric_data[DisList]) {
    distric_data[DisList].forEach(function (thana) {
          thanaOptions += '<option value="' + thana + '">' + thana + '</option>';
      });
  }

  document.getElementById("polic_sta").innerHTML = thanaOptions;
}

$(document).ready(function() {
  // Function to handle AJAX and element visibile


  function sectionChosen() {
      const sectionData = $("#select-country-input-3").val();
      console.log(sectionData);

      if (sectionData === "outsideBangladesh") {
          $("#divisionSection").hide();
          $("#citySection").hide();
          $("#areaSection").hide();
          // Hide relevant sections for outside Bangladesh
          $("#OutsideBangladeshPayment").show();
          $("#CashOnDeliveryPayment").hide();
          $("#CashWithMobileWalletPayment").hide();
          $("#CashWithCardPayment").hide();
      } else {

          $("#divisionSection").show();
          $("#citySection").show();
          $("#areaSection").show();
          // Show relevant sections for Bangladesh
          $("#OutsideBangladeshPayment").hide();
          $("#CashOnDeliveryPayment").show();
          $("#CashWithMobileWalletPayment").show();
          $("#CashWithCardPayment").show();
      }
  }

  // Bind the function to a change event or call directly if needed
  $("#select-country-input-3").on("change", sectionChosen);

  // Call function initially if you need to apply on page load
  //sectionChosen();
});





