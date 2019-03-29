## SPD Dataset Description File

**Description**
We provide a set of spam and non-spam dataset collected from Twitter beginning from late 2016.
The dataset consists of 9000 predicted spam accounts (labelled 0) and 8515 non-spam accounts (labelled 1) based on the method proposed in ‘Detection of Spam-posting Accounts on Twitter’.

**Data Format**
The SPD dataset is in a .csv file format (named spd-dataset_01_ids.csv) consisting of spam (0) and non-spam (1) accounts’ identification number. We also provide a basic python script (in Jupyter Notebook) that will enable collection of the data using Twitter’s API. The following fundamental features (which could be used to define other features, please see the research article below for the full features) are included in the script:

 - UserID: numeric identifier of the account user
 - ScreenName: screen-name of the user
 - AccountCreated: account creation time (used together with TweetCreatedAt to define AccountAge Feature)
 - TweetCreatedAt: collection date of the most recent tweet from an account
 - Description: a brief textual description provided by the account user
 - TweetFavouriteCount: number of likes from the user
 - FollowersCount: number of other users following the account owner
 - FriendsCount: number of users the account owner is following
 - StatusesCount: total number of activities e.g. tweeting, RT, etc.
 - Tweets: sample tweets produced by the account

**Publications using the dataset**
* Inuwa-Dutse, I., Liptrott, M. and Korkontzelos, I., 2018. Detection of spam-posting accounts on Twitter. Neurocomputing, 315, pp.496-511.
* Inuwa-Dutse, I., 2018, April. Modelling Formation of Online Temporal Communities. In Companion of the The Web Conference 2018 on The Web Conference 2018 (pp. 867-871). International World Wide Web Conferences Steering Committee.

**Citing Articles**
* Pandey, A.C. and Rajpoot, D.S., 2019. Spam review detection using spiral cuckoo search clustering method. Evolutionary Intelligence, pp.1-18.
* R, Vinayakumar & Alazab, Mamoun & Jolfaei, Alireza & Kp, Soman & Poornachandran, Prabaharan. (2018). Ransomware Triage Using Deep Learning: Twitter as a Case Study.
* Inuwa-Dutse, Isa & Bello, Bello & Korkontzelos, Ioannis. (2018). Lexical analysis of automated accounts on Twitter.
* Inuwa-Dutse, I., Bello, B.S. and Korkontzelos, I., 2018. THE EFFECT OF ENGAGEMENT INTENSITY AND LEXICAL RICHNESS IN IDENTIFYING BOT ACCOUNTS ON TWITTER. IADIS International Journal on WWW/Internet, 16(2).

**Citation Format** Please cite the work (if any part of the work is relevant and utilised in your research) as follow:
* Inuwa-Dutse, I., Liptrott, M. and Korkontzelos, I., 2018. Detection of spam-posting accounts on Twitter. Neurocomputing, 315, pp.496-511.

Contact: For further questions please contact: [email](dutsei@edgehill.ac.uk)

