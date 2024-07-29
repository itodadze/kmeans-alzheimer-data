# აბსტრაქტი

პროექტის ძირითად მიზანს წარმოადგენდა დემენციის სხვადასხვა ფორმის მქონე ადამიანებში გენთა ექსპრესიის გარკვეული პატერნების აღმოჩენა. პროექტის განსახორციელებლად გამოვიყენეთ Clusterization ალგორითმი, თუმცა დამხმარე ბიბლიოთეკები არ გამოგვიყენებია ვინაიდან sampleთა რაოდენობა არ იყო განსაკუთრებულად ბევრი. გამოვავლინეთ საინტერესო გენეტიკური განმასხვავებლები სხვადასხვა დემენციის ფორმის მქონე ადამიანებში.

დავაჯგუფეთ 2 და 3 ჯგუფებად დაახლოებით 3000 სხვადასხვა miRNA მათი ექსპრესიის დონის მიხედვით და გაფილტვრის შედეგად აღმოვაჩინეთ დაახლოებით 20-30 miRNA, რომელთა ექსპრესიის სხვადასხვა დონის მიხედვით შეგვიძლია აღმოვაჩინოთ მკვეთრი კორელაცია ადამიანების დიაგნოზთან (ან დიაგნოზის არ არსებობასთან).

პროექტის შედეგად გამოვლენილი საინტერესო გენეტიკური მარკერები შეიძლება რომ გაანალიზდეს ბიოლოგიურად და დადგინდეს კონკრეტული მიზეზ-შედეგობრიობის პატერნები სხვადასხვა miRNA-თა ექსპრესიათა და დაავადებებს შორის. 

# პროექტის მიმოხილვა
ამ პროექტის ფარგლებში დავამუშავეთ 2019 წელს გამოქვეყნებული კვლევიდან მიღებული 1601 იაპონელი ადამიანის გენეტიკური ინფორმაცია.  ამ პიროვნებების ნაწილი დაავადებული იყო დემენციის სხვადასხვა ფორმით (ალცჰაიმერი, ვასკულარული დემენცია და ა.შ). ჩვენი მიზანი იყო შეგვესწავლა მოცემული მასალა, მოგვეხდინა კლასტერიზაცია და აღმოგვეჩინა კავშირები დემენციის სხვადასხვა ფორმასა და კონკრეტული გენების ექსპრესიას შორის. 

# გამოყენებული სტატია:
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE120584
 
# ნაბიჯები პროექტის გასაშვებად: 
    1. საიტიდან გადმოვწეროთ GSE120584_RAW.tar, ამოვაარქივოთ და ჩავაგდოთ data ფოლდერში
    2. cd fetcher
    3. python __main__.py
    4. cd processor
    5. python __main__.py
    6. cd sorter
    7. python __main__.py
    8. cd kmeans
    9. python __main__.py

# Pipeline

   - fetch - საიტს https://www.ncbi.nlm.nih.gov/ ვუკეთებთ parsing-ს და data/table.txt ფაილში ვინახავთ ინფორმაციას კვლევაში მონაწილე ადამიანების ასაკის, სქესის, დიაგნოზისა და დნმ-ში APOE4 ალელის რაოდენობის შესახებ.
   - Process – GSE120584_RAW.tar -ში მოთავსებულ ფაილებს ვამუშავებთ და data/GSE120584_PROCESSED ფოლდერში ვათავსებთ ახალ ფაილებს, რომლებიც დაცლილია ზედმეტი ინფორმაციისაგან. ისინი მოიცავს დატას კვლევის თითოეული მონაწილის ორგანიზმში კონკრეტული (3000-ზე მეტი) გენების ექსპრესიის დონეების შესახებ. 
   - Sort - data/GSE120584_PROCESSED ფოლდერში ინფორმაცია ფაილებში ექსპერიმენტის მონაწილეების უნიკალური იდენტიფიკატორების მიხედვით გვაქვს გადანაწილებული. ამ ნაბიჯის შემდეგ data/GSE120584_SORTED ფოლდერში ვიღებთ ფაილებს, რომლებიც გენების მიხედვითაა დაყოფილი და თითოეულ მათგანში გვხვდება ინფორმაცია, კვლევაში მონაწილე ადამიანებში რა დონეზე ხდება კონკრეტული გენის ექსპრესია. 
   - Filter - უშუალოდ კლასტერიზაციის ეტაპი. data/GSE120584_RESULTS ფოლდერებში კონკრეტული გენებისთვის ვიღებთ ინფორმაციას კლასტერების შესახებ: მასში შემავალი ადამიანების საშუალო ასაკი, გენის ექსპრესიის დონე, სქესთა შორის გადანაწილება და ა.შ. ამ დატას გამოყენებით ვადგენთ კავშირებს დემენციის ფორმებსა და გენთა ექსპრესიას შორის. 

# კლასტერიზაცია
ინფორმაციის დასამუშავებლად გადავწყვიტეთ k-means კლასტერიზაციის ალგორითმის გამოყენება. ჩვენი თავდაპირველი მიდგომა იყო, რომ ყველა გენი, 3000 მათგანი, განგვეხილა ერთად და ასე მიღებული დატა გაგვეანალიზებინა, რაც 3000 განზომილებაში მუშაობას გულისხმობდა (ზოგადად კლასტერიზაცია 1-3 განზომილებაში სრულდება ხოლმე). ეს არ აღმოჩნდა ეფექტური, ამიტომ გადავწყვიტეთ სხვა მეთოდიც გვეცადა. თითოეული გენისთვის ცალცალკე გავაკეთეთ კლასტერიზაცია, თუმცა საბოლოოდ შედეგებში ყველა მათგანი არ დავტოვეთ. data/GSE120584_RESULTS  ფოლდერში მხოლოდ იმ გენების შესახებ გვაქვს ფაილები, რომლების კლასტერებიც ერთმანეთისაგან საგრძნობლად განსხვავდება. მაგალითად არ დავტოვეთ ინფორმაცია ისეთ გენებზე, რომლებშიც სქესის მიხედვით გადანაწილება კლასტერებში ჰგავდა ერთმანეთს, რადგან ასე რაიმე ახლის აღმოჩენა ფაქტობრივად შეუძლებელიც იყო. ინფორმაცია დავამუშავეთ 2 და 3 კლასტერის არსებობის პირობებში. მიღებულ შედეგებს შეხვდებით data/GSE120584_RESULTS_2 და data/GSE120584_RESULTS_3 საქაღალდეებში. 

# მიღებული შედეგები
ჩვენ დავამუშავეთ სტატიაში მოცემული ინფორმაცია მიკრო რნმ-ების შესახებ, ანუ რნმ-ის მოკლე არამაკოდირებელი უბნების შესახებ, რომლებიც მთავარი ფუნქციაც ცილების სინთეზის, ანუ გენთა ექსპრესიის დათრგუნვაა. განვიხილოთ რამდენიმე მათგანი და დავაკავშიროთ მიღებული შედეგები დემენციის სხვადასხვა ტიპთან.

## hsa-miR-24-3p
ჩვენს საკვლევ საკითხთან დაკავშირებით რელევანტური იქნება შემდეგი კავშირები:
  1. BACE1 - ეს ენზიმი ჩართულია ბეტა-ამილოიდ პეპტიდების წარმოებაში. მათი ზედმეტი რაოდენობით დაგროვება ორგანიზმში დამახასიათებელია ალცჰაიმერის დაავადებისათვის. ეს მიკრო რნმ დემენციით დაავადებულ ადამიანებში უფრო მეტად გვხვდება, რადგან ბეტა-ამილოიდ პეპტიდების შემცირება ხდება საჭირო სხეულში.  
  2.  ნეირონული ანთება - მიკრო რნმ has-miR-24-3p მონაწილეობს იმ გენების ექსპრესიის რეგულაციაში, რომლებიც ანთებით პროცესებშია ჩართული. ქრონიკული ნეირონული ანთებითი პროცესები დამახასიათებელია ალცჰაიმერისათვის, ამიტომ შესაძლებელია, რომ სწორედ ამის სამართავად იზრდება ორგანიზმში ამ მიკრო რნმ-ს რაოდენობა.  
  3. APOE4 -  ცნობილი ფაქტია, რომ ორგანიზმში APOE4 ალელის არსებობა, ზრდის ალცჰაიმერის რისკს. APOE4-სა და hsa-miR-24-3p-ს შორის უკუპროპორციული დამოკიდებულება არსებობს. იმ ადამიანებში, ვისაც არ აქვთ APOE4, has-miR-24-3p უფრო დიდი რაოდენობით ექსპრესირდება. ისეთ ადამიანებს, ვისაც APOE4 ალელი აქვთ, ამ მიკრო რნმ-ს დიდი რაოდენობა დასჭირდებათ, ბეტა-ამილოიდ პეპტიდების დასარეგულირებლად ორგანიზმში, თუმცა სამწუხაროდ მათში ექსპრესია პირიქით ნაკლებად მოხდება. ეს აღმოჩენილი კავშირი შეიძლება იყოს მიზეზი იმისა, თუ რატომ ასოცირდება APOE4 ალცჰაიმერთან. 

## hsa-miR-345-3p
   1. BACE1 - ეს მიკრო რნმ-ც მონაწილეობს ბეტა-ამილოიდ პეპტიდების რეგულაციაში. has-miR-345-3p საგრძნობლად მაღალია იმ ადამიანებში, რომლებსაც აქვთ DLB (dementia with lewy bodies).
   2. SNCA - ეს გენი ალფა-სინუკლეინის წარმოებაზეა პასუხისმგებელი. ალფა-სინუკლეინის ზედმეტი რაოდენობით დაგროვება ორგანიზმში DLB-ისთვისაა დამახასიათებელი. Has-miR-345-3p სწორედ SNCA გენის ექსპრესიას თრგუნავს. 

## hsa-miR-153-5p
   1. BACE1 - ეს მიკრო რნმ ასევე მონაწილეობას იღებს BACE1-ის რეგულაციაში. წინა მიკრო რნმ-ების მსგავსად, hsa-miR-153-5p უფრო დიდი რაოდენობით დემენციის სხვადასხვა ფორმის მქონე ადამიანებში ექსპრესირდება. 
   2. ოქსიდაციური სტრესი - ეს არის მდგომარეობა, რომელსაც ორგანიზმში ანტიოქსიდანტების ნაკლებობა იწვევს. hsa-miR-153-5p გავლენას ახდენს ანტიოქსიდანტების ინჰიბირებაზე. ოქსიდაციური სტრესი ალცჰაიმერის დროს მიმდინარე ნეირონულ დაზიანებასთანაა კავშირში. ამ შემთხვევაში hsa-miR-153-5p, სხვა მიკრო რნმ-ებისგან განსხვავებით, ხელს უშლის ორგანიზმს დაავადებასთან გამკლავებაში და სიმპტომებთან ბრძოლაში. შეიძლება ვივარაუდოთ, რომ იმ ადამიანებში უფრო ხშირად ვითარდება ალცჰაიმერი, რომლებიც ამ მიკრო რნმ-ს უფრო დიდი რაოდენობით აწარმოებენ, ვიდრე დანარჩენებში. ეს მიკრო რნმ შეიძლება გარკვეულწილად გამომწვევ მიზეზადაც კი აღვიქვათ. 

## hsa-miR-4720-3p
ეს მიკრო რნმ-ც უფრო დიდი რაოდენობით წარმოდგენილია დემენციის რომელიმე ფორმით დაავადებულ ადამიანებში, ვიდრე დანარჩენებში. 
   1. BACE1
   2. ნეირონული ანთება

რომ შევაჯამოთ, k-means კლასტერიზაციის გამოყენებით დავამუშავეთ საკმაოდ დიდი ინფორმაცია და ვიპოვეთ კავშირები მიკრო რნმ-ებსა და დემენციის გარკვეულ ფორმებს შორის. ხშირად ეს კავშირი იმით აიხსნებოდა, რომ დაავადების დროს ორგანიზმში გარკვეული ნივთიერებების რეგულაცია ხდებოდა საჭირო, რაც მიკრო რნმ-ს ექსპრესიას ზრდიდა, თუმცა ზოგ შემთხვევაში შევძელით იმ დასკვნის გაკეთება, რომ ამ მიკრო რნმ-ს ექსპრესიამ შეიძლება ალცჰაიმერის რისკი გაზარდოს ადამიანებში და ერთგვარად მისი გამომწვევიც კი გახდეს. 
