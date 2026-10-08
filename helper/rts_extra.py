# Notes:
import sys
import json
from pathlib import Path
from typing import Any

# Add project root to sys.path (find the directory containing db_structs.py)
_root = Path(__file__).resolve().parent
while _root.parent != _root:
    if (_root / "db_structs.py").exists():
        if str(_root) not in sys.path:
            sys.path.append(str(_root))
        break
    _root = _root.parent

from db_structs import (
    Medium,
    Circle,
    Event,
    EventGroup,
    Source,
    ReliabilityTypes,
    OriginTypes,
    Location,
)

RT, OT = ReliabilityTypes, OriginTypes

PATH_HELPER = Path(__file__).parent
PATH_EVENT_GROUP = PATH_HELPER.parent
PATH_MEDIA = PATH_EVENT_GROUP / "media"


def retrieve_circles(event_name: str) -> list[Circle]:
    """Retrieve circles of given event. In the circle file has not been created, execute the creation script first."""
    circles_json_path = PATH_HELPER / event_name / "circles.json"
    if not circles_json_path.exists():
        print(
            f"Circle file for {event_name} not found, running the creation script ..."
        )
        creation_script_path = PATH_HELPER / event_name / "main.py"
        if not creation_script_path.exists():
            raise FileNotFoundError(
                f"Creation script for {event_name} not found at {creation_script_path}"
            )
        # Import main() from the creation script and execute
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            f"{event_name}.main", creation_script_path
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "main"):
                module.main()

        if not circles_json_path.exists():
            raise FileNotFoundError(
                f"Creation script {creation_script_path} failed to create {circles_json_path}"
            )

    with circles_json_path.open("r", encoding="utf-8") as f:
        circles_raw = json.load(f)
    return [Circle.load_from_json(c) for c in circles_raw]


if __name__ == "__main__":
    events: list[Event] = []
    disabled_events: list[int | str] = []

    thwikicc = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E7%A7%8B%E5%AD%A3%E4%BE%8B%E5%A4%A7%E7%A5%AD"

    i = "sp1"  # ==== rts_sp1 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_sp1 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%ADSP/%E7%AC%AC1%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "sp_reitaisaisp_bnr.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20110108031108/http://www.reitaisai.jp/img/reitaisaisp_bnr.jpg",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "sp_sp.JPG",
                [
                    Source(
                        "https://web.archive.org/web/20110226113125/http://reitaisai.jp/img/sp.JPG",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(35.6284445, 139.7926734),
                address="3 Chome-11-1 Ariake, Koto City, Tokyo 135-0063, Japan",
                description="東京ビッグサイト 東4・5・6ホール",
                sources=[
                    Source(
                        "https://web.archive.org/web/20101008040306/http://www.reitaisai.jp/outline.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWmniRNV84lzB1SNXuy60c0lznxgbqmNtYyJ8rkHQXk9u4qwSBeDafMEeWY7SaHOPcgw9m9BObYv4SvxJATFOtwEErABiE-oZjeBkl96ni8hTFClnpIJNnLLpRCBg6Ue9K__BWAAVQ=s0?imgmax=0",
                url="https://maps.app.goo.gl/6EYu64eY7PRhWRxu7",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭SP",
                "博麗神社例大祭SP",
                "Hakurei Jinja Reitaisai SP",
                "Reitaisai SP",
                "RTS SP",
                "博麗神社例大祭 (スペシャル)",
                "Hakurei Jinja Reitaisai Special",
                "RTS SP1",
            ],
            dates="2010.09.19",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20101008040306/http://www.reitaisai.jp/outline.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20100703080700/http://reitaisai.jp/result.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_sp1} (well sourced)",
                    (ReliabilityTypes.Reliable, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.06",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "sp2"  # ==== rts_sp2 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_sp2 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%ADSP/%E7%AC%AC2%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(35.6284445, 139.7926734),
                address="3 Chome-11-1 Ariake, Koto City, Tokyo 135-0063, Japan",
                description="東京ビッグサイト",
                sources=[
                    Source(
                        "https://web.archive.org/web/20111109155922mp_/http://www.reitaisai.jp/outline.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWmniRNV84lzB1SNXuy60c0lznxgbqmNtYyJ8rkHQXk9u4qwSBeDafMEeWY7SaHOPcgw9m9BObYv4SvxJATFOtwEErABiE-oZjeBkl96ni8hTFClnpIJNnLLpRCBg6Ue9K__BWAAVQ=s0?imgmax=0",
                url="https://maps.app.goo.gl/6EYu64eY7PRhWRxu7",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭SP2",
                "博麗神社例大祭SP2",
                "Hakurei Jinja Reitaisai SP2",
                "Reitaisai SP2",
                "RTS SP2",
                "博麗神社例大祭 (スペシャル2)",
                "Hakurei Jinja Reitaisai Special 2",
            ],
            dates="2011.09.11",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20111109155922mp_/http://www.reitaisai.jp/outline.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20111123184511/http://reitaisai.jp/circlelists/search/circles/0",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_sp2} (well sourced)",
                    (ReliabilityTypes.Reliable, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.08",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "tw1"  # ==== rts_tw1 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_tw1 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E5%8F%B0%E6%B9%BE/%E7%AC%AC1%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "tw1_rtstw1.jpg",
                [Source(thwikicc_tw1, (ReliabilityTypes.Likely, OriginTypes.External))],
            ),
            Medium(
                "tw1_RTSTW_map-265x300.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20150526041319/http://reitaisai.com/rtstw/circle-list",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(25.0617771, 121.4914951),
                address="No. 2, Section 1, New Taipei Blvd, Zhongshan Village, Sanchong District, New Taipei City, Taiwan 241",
                description="三重区綜合体育館",
                sources=[
                    Source(
                        "https://web.archive.org/web/20150625154819/http://reitaisai.com/rtstw/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/ANWiy9SUhEIH7yhJ6MMhvx8gglEc-Y_3jnsCdrh61JHSozlObZgQ6ChpBjoiedKKKfGpRG0utO5y1-YcZZmv5Kic8f8_JNEGpjqIwkO8PR6GIMQpnM7T5n4-78jiWOWmprtJ0QiMFGlg=s0?imgmax=0",
                url="https://maps.app.goo.gl/jhWDgcEd63Se7M3V6",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭in台灣1",
                "博麗神社例大祭in台灣1",
                "Hakurei Jinja Reitaisai in Taiwan 1",
                "Reitaisai in Taiwan 1",
                "RTS TW1",
                "第一回博麗神社例大祭in台灣",
            ],
            dates="2015.06.06",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20150625154819/http://reitaisai.com/rtstw/",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20150526041319/http://reitaisai.com/rtstw/circle-list",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_tw1} (not sourced)",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.08",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "tw1.5"  # ==== rts_tw1.5 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_tw1_5 = "https://thwiki.cc/%E5%B1%95%E4%BC%9A%E4%BD%9C%E5%93%81%E5%88%97%E8%A1%A8?e=%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E5%8F%B0%E6%B9%BE%231_5"

        media_ = [
            Medium(
                "1.5_rts1.5.jpg",
                [
                    Source(
                        thwikicc_tw1_5, (ReliabilityTypes.Likely, OriginTypes.External)
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(25.0216697, 121.5352956),
                address="No. 1號, Section 4, Roosevelt Rd, Xuefu Village, Da’an District, Taipei City, Taiwan 106",
                description="台湾大学綜合体育館１階",
                sources=[
                    Source(
                        "https://live.nicovideo.jp/watch/lv252981576",
                        (ReliabilityTypes.Reliable, OriginTypes.OfficialExt),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/ANWiy9TgQ77cRam5Gc-B66TLwY_1lp5cvWrkZXd9sTteRFItUFA7Oip4oOU4n38sxDYiRIG0jFGPDAtXTaorMrQ7Hte97lcHIOw9zu_jMM3M8VP4ZBmIfn5KCQNP5omab40ei_Qk529j=s0?imgmax=0",
                url="https://maps.app.goo.gl/a9rCjTYbVyUtwxMB9",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭in台灣1.5",
                "博麗神社例大祭in台灣1.5",
                "Hakurei Jinja Reitaisai in Taiwan 1.5",
                "Reitaisai in Taiwan 1.5",
                "RTS TW1.5",
            ],
            dates="2016.02.21",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://live.nicovideo.jp/watch/lv252981576",
                    (ReliabilityTypes.Reliable, OriginTypes.OfficialExt),
                ),
                Source(
                    "Other source, TW1.5 alias: https://thwiki.cc/%E5%B1%95%E4%BC%9A%E4%BD%9C%E5%93%81%E5%88%97%E8%A1%A8?e=%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E5%8F%B0%E6%B9%BE%231_5",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
                Source(
                    "Main URL (dead) referenced here: https://x.com/HakureijinjyaS/status/700969067671195649",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
                Source(
                    "Participating circles (day 1): https://web.archive.org/web/20160408114127/http://gjs.tw/ch/group_list.html",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles (day 2): https://web.archive.org/web/20160226150433/http://gjs.tw/ch/group_list2.html",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            description="Part of the 2016 edition of Comic Horizon.",
            comments='I could not find any evidence of the "TW1.5" alias, but it probably still should be included in the RTS database.',
            last_edited="2026.10.08",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "tw2"  # ==== rts_tw2 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_tw2 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E5%8F%B0%E6%B9%BE/%E7%AC%AC2%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "tw2_rtstw2.jpg",
                [
                    Source(
                        thwikicc_tw2, (ReliabilityTypes.Reliable, OriginTypes.Official)
                    )
                ],
            ),
            Medium(
                "tw2_2bc525_3b1e389cb0604fc88e410e4c096ddcdc~mv2_d_2738_1208_s_2.avif",
                [
                    Source(
                        "https://afongcp.wixsite.com/rtstw2/clist",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "tw2_2bc525_54007ee9b2d942c3971066bd90a1ca87~mv2_d_2185_1575_s_2.avif",
                [
                    Source(
                        "https://afongcp.wixsite.com/rtstw2", (RT.Reliable, OT.Official)
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(25.0725177, 121.5182936),
                address="No. 232, Section 3, Chengde Rd, Bao'an Village, Datong District, Taipei City, Taiwan 103",
                description="台灣台北市大同區承德路三段232號B1,B2(橡木桶洋酒旁)",
                sources=[
                    Source(
                        "https://afongcp.wixsite.com/rtstw2/map",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://streetviewpixels-pa.googleapis.com/v1/thumbnail?panoid=29YYFfX8ISuW4-rg6412eA&cb_client=search.gws-prod.gps&w=612&h=360&yaw=283.37595&pitch=-30&thumbfov=100",
                url="https://maps.app.goo.gl/gqKSczgxDXZtZMPLA",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭in台灣2",
                "博麗神社例大祭in台灣2",
                "Hakurei Jinja Reitaisai in Taiwan 2",
                "Reitaisai in Taiwan 2",
                "RTS TW2",
                "第二回博麗神社例大祭in台灣",
            ],
            dates="2017.05.28",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://afongcp.wixsite.com/rtstw2/about",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://afongcp.wixsite.com/rtstw2/clist",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_tw2} (well sourced)",
                    (ReliabilityTypes.Reliable, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.08",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    # i =   # ==== rts_ ====
    # if i not in disabled_events:
    #     event_name = f"rts_{i}"
    #     print(f"Processing {event_name} ...")

    #     media_ = [
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #     ]
    #     locations = [
    #         # Location(
    #         #     coordinates=(,),
    #         #     address="",
    #         #     description="",
    #         #     sources=[Source("", (ReliabilityTypes.Reliable, OriginTypes.Official))],
    #         #     # comments=None,
    #         #     imageUrl="",
    #         #     url="",
    #         # ),
    #     ]
    #     event = Event(
    #         aliases=,
    #         dates="",
    #         circles=[],
    #         media=media_,
    #         sources=[
    #             # Source("Date: ", (RT.Reliable, OT.Official)),
    #             # Source("Participating circles: ", (RT.Reliable, OT.Official)),
    #         ],
    #         locations=locations,
    #         description=None,
    #         # comments=None,
    #         last_edited="2026.10.06",
    #     )

    #     # Retrieve circles
    #     # event.circles = retrieve_circles(event_name)
    #     events.append(event)

    # ==== event group ====
    media = [
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
    ]
    links = [
        "https://reitaisai.com/",
        "https://x.com/HakureijinjyaS",
        "https://www.youtube.com/channel/UCWgWAk02r-HKSYX2h6wnJVA",
        "https://x.com/reitaisai_sp",
    ]

    event_group = EventGroup(
        aliases=[
            "博麗神社例大祭 (other events)",
            "Hakurei Jinja Reitaisai (other events)",
            "秋季例大祭 (other events)",
            "Reitaisai (other events)",
            "RTS (other events)",
        ],
        events=[],
        media=media,
        links=links,
        description="Collection of RTS (博麗神社例大祭) events not of the main numbered series, such as the SP (Special) events.",
        last_edited="2026.10.08",
    )

    print(f"Saving {Path(__file__).stem} database...")
    event_group.save(PATH_EVENT_GROUP, indent=None)
    print("Done")
