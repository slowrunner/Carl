I Git This
==========

What (Git-managed) projects/code/document have you been working on since a
month? Just ask!

```
$ git-done last month

Git activity on the 2016-01-15:
debian-packages:
-- 3 commits in dlib-18.18
src:
-- 7 commits in academia-website
-- 17 commits in gazr

Git activity on the 2016-01-16:
debian-packages:
-- 1 commits in dlib-18.18

Git activity on the 2016-01-17:
None

[...]
```

And yesterday?

```
$ git-done yesterday

Git activity on the 2016-02-15:
publications:
-- 11 commits in icra-2016-cellulo-localization

Git activity on the 2016-02-16:
publications:
-- 3 commits in icra-2016-cellulo-localization
src:
-- 3 commits in attention_tracker

Git activity on the 2016-02-17:
src:
-- 3 commits in academia-website
-- 3 commits in rpi-config

Git activity on the 2016-02-18:
None

[...]
```

Magic!


This small shell script (bash) does the following:

- for every day since the provided starting date:
    - iterate over all your git repositories in your `$HOME`
    - count how many commits you did that day (on any branch)
    - (optionally) send the summary to your [IDoneThis](https://idonethis.com) account

Usage
-----

```sh
$ ./git-done <starting date>
```

The starting date can be anything that GNU `date` can interpret: for instance,
`last week`, `yesterday`, `2016-01-12`,  `a month ago` all work.

If you want to post the summaries to IDoneThis, simply fill in the `api_token`
and `team_name` variables at the top of the script.

*The script does not yet check if you have already posted a summary for the
given days: if you run the script several times, summaries will be posted
several times! PR welcome :-)*

Dependencies
------------
For OS X users, please install `coreutilities` to be able to use GNU `date`.
```
homebrew install coreutilities
```
