#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json
import os
import time
import praw

from tqdm import tqdm
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from praw.models import MoreComments

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

########################################
# CONFIG
########################################

SUBREDDIT = (
"Microsoft","teslamotors","apple","google","amazon",
"facebook","linkedin","snapchat","Tiktokhelp","reddit",
"intel","adobe","oracle","ibm","salesforce",
"walmart","Costco","Ebay","Etsy","Target",
"Toyota","BMW","Ford","Porsche","Honda",
"boeing","airbus","spacex","nasa",
"Chase","paypal","Robinhood","CoinBase",
"bitcoin","ethereum",
"netflix","disney","spotify","hulu","paramountplus",
"steam","nintendo","playstation","xbox",
"McDonalds","starbucks","Dominos","Chipotle",
"Uber","Airbnb"
)

MONTHS = 6
POST_LIMIT = 900000000
TARGET_GROUPS = 50000

AUTOSAVE_EVERY = 20

CSV_FILE = "c2c_conflicts.csv"
JSON_FILE = "c2c_conflicts.json"
CHECKPOINT_FILE = "crawler_checkpoint.json"

########################################
# REDDIT
########################################

def init_reddit():

    return praw.Reddit(
        client_id = os.environ["REDDIT_CLIENT_ID"],
        client_secret = os.environ["REDDIT_CLIENT_SECRET"],
        user_agent="c2c_conflict_research_script",
        username = os.environ["REDDIT_USERNAME"],
        password = os.environ["REDDIT_PASSWORD"],
        ratelimit_seconds=5
    )



########################################
# CHECKPOINT
########################################

def load_checkpoint():

    if not os.path.exists(CHECKPOINT_FILE):
        return set()

    with open(CHECKPOINT_FILE,"r") as f:
        data = json.load(f)

    return set(data)

def save_checkpoint(seen_posts):

    with open(CHECKPOINT_FILE,"w") as f:
        json.dump(list(seen_posts),f)

########################################
# COMMENT TREE
########################################

def load_tree(submission):

    try:
        submission.comments.replace_more(limit=None)
    except:
        return {},{}

    by_id={}
    children={}

    stack=list(submission.comments)

    while stack:

        c=stack.pop()

        if isinstance(c,MoreComments):
            continue

        by_id[c.id]=c

        parent=c.parent_id.split("_")[-1]

        children.setdefault(parent,[]).append(c.id)

        stack.extend(list(c.replies))

    return by_id,children

########################################
# CONVERSATION KEY
########################################

def conversation_key(seq):

    ids=[c.id for c in seq]
    return "-".join(ids)

########################################
# DETECT CONFLICT
########################################

def detect_conflicts(by_id, children, mods):

    sequences = []

    for cid, comment in by_id.items():

        if not comment.author:
            continue

        author1 = str(comment.author).lower()

        if author1 in mods:
            continue

        for r1_id in children.get(cid, []):

            r1 = by_id[r1_id]

            if not r1.author:
                continue

            author2 = str(r1.author).lower()

            if author2 in mods or author2 == author1:
                continue

            for r2_id in children.get(r1_id, []):

                r2 = by_id[r2_id]

                if not r2.author:
                    continue

                mod = str(r2.author).lower()

                if mod not in mods:
                    continue

                ux_found = False

                for r3_id in children.get(r2_id, []):

                    r3 = by_id[r3_id]

                    if not r3.author:
                        continue

                    author3 = str(r3.author).lower()

                    if author3 in mods:
                        continue

                    ux_found = True

                    sequences.append([comment, r1, r2, r3])

                # 如果 M 有多个回复 Ux，这里不会限制数量

    return sequences

########################################
# USER ANONYMIZATION
########################################

def anonymize(seq,mods):

    mapping={}
    counter=1

    for c in seq:

        if not c.author:
            continue

        name=str(c.author)

        if name.lower() in mods:
            continue

        if name not in mapping:

            mapping[name]=f"user_{counter}"
            counter+=1

    return mapping

########################################
# SAVE DATA
########################################

def save_results(groups):

    dataset_json=[]

    with open(CSV_FILE,"w",newline="",encoding="utf-8") as f:

        writer=csv.writer(f)

        writer.writerow([
        "group_id","step","role","author",
        "time","comment_id","parent_id","text"
        ])

        gid=1

        for post,seq in groups:

            writer.writerow([])
            writer.writerow([f"========== GROUP {gid} =========="])

            mods={str(m).lower() for m in post.subreddit.moderator()}

            user_map=anonymize(seq,mods)

            record=[]

            step=1

            for c in seq:

                if not c.author:

                    role="unknown"
                    author="[deleted]"

                else:

                    name=str(c.author)

                    if name.lower() in mods:

                        role="moderator"
                        author=name

                    else:

                        role="user"
                        author=user_map[name]

                row=[
                gid,
                step,
                role,
                author,
                datetime.fromtimestamp(
                c.created_utc,timezone.utc).isoformat(),
                c.id,
                c.parent_id.split("_")[-1],
                c.body.replace("\n"," ")
                ]

                writer.writerow(row)
                record.append(row)

                step+=1

            dataset_json.append(record)

            gid+=1

    with open(JSON_FILE,"w") as f:
        json.dump(dataset_json,f,indent=2)

########################################
# MAIN
########################################

def main():

    reddit=init_reddit()

    cutoff=datetime.now(timezone.utc)-relativedelta(months=MONTHS)
    cutoff_ts=cutoff.timestamp()

    seen_posts=load_checkpoint()

    groups=[]
    seen_conv=set()

    post_counter=0

    start=time.time()

    try:

        for sub_name in SUBREDDIT:

            print(f"\nScanning r/{sub_name}")

            subreddit=reddit.subreddit(sub_name)

            try:
                mods={str(m).lower() for m in subreddit.moderator()}
            except:
                mods=set()

            for post in tqdm(subreddit.new(limit=POST_LIMIT)):

                if post.id in seen_posts:
                    continue

                seen_posts.add(post.id)

                post_counter+=1

                if post.created_utc < cutoff_ts:
                    continue

                if post.num_comments < 4:
                    continue

                try:

                    by_id,children=load_tree(post)

                    seqs=detect_conflicts(by_id,children,mods)

                except Exception:
                    continue

                for seq in seqs:

                    key=conversation_key(seq)

                    if key in seen_conv:
                        continue

                    seen_conv.add(key)

                    groups.append((post,seq))

                    elapsed=time.time()-start
                    rate=len(groups)/elapsed if elapsed>0 else 0
                    eta=(TARGET_GROUPS-len(groups))/rate if rate>0 else 0

                    print(
                    f"\nFOUND {len(groups)} | "
                    f"posts:{post_counter} | "
                    f"ETA:{int(eta/60)} min"
                    )

                    if len(groups)%AUTOSAVE_EVERY==0:

                        save_results(groups)
                        save_checkpoint(seen_posts)

                        print("Autosaved")

                    if len(groups)>=TARGET_GROUPS:
                        raise KeyboardInterrupt

    except KeyboardInterrupt:

        print("\nStopping crawler...")

    print("\nSaving final dataset...")

    save_results(groups)
    save_checkpoint(seen_posts)

    print("\n===== FINAL STATS =====")
    print("Posts scanned:",post_counter)
    print("Conversations:",len(groups))

########################################

if __name__=="__main__":
    main()