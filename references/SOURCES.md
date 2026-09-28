# BDX droid reference images: sources

All files were downloaded on 2026-09-26. Each one was checked as a real image (magic bytes via `file`, opened with PIL, size > 5 KB).
Images are copyrighted by their respective owners (Disney, NVIDIA, news outlets, fan blogs, and open-source projects). Use them for private CAD reference only.

Note: `video/` is a separate folder of video frames made by another process. It is not listed here.

## YourStory article (task 1)
Page: https://yourstory.com/2025/03/nvidia-google-deepmind-power-disneys-adorable-ducks
The raw HTML was checked for og:image, img src/srcset/data-src and the Next.js JSON. The article body has **one** image, the hero, which is also the og:image. Every other image on the page is site chrome (logos, author avatars, "Google Preferred" badge) or belongs to other articles.

| File | Source URL |
|---|---|
| 01_yourstory_hero_original.jpg | https://images.yourstory.com/cs/2/e35953e0c10a11eeaef14be6ff40ae87/Imageup9g-1742488673441.jpg |

## Disney Research paper: "Design and Control of a Bipedal Robotic Character" (Grandia et al., RSS 2024, arXiv 2501.05204)
Paper: https://arxiv.org/abs/2501.05204 · PDF: https://arxiv.org/pdf/2501.05204 · HTML: https://arxiv.org/html/2501.05204v1
Files marked "PDF p.N" were extracted at full resolution from the images embedded in the PDF.

| File | Source |
|---|---|
| 04_paper_exploded_view_hires.png | PDF p.3 (Fig. 3, exploded mechanical design). Low-res copy: https://arxiv.org/html/2501.05204v1/bd2_exploded_view_colorized_v2.png |
| 05_paper_path_frame_standing.jpg | https://arxiv.org/html/2501.05204v1/figures/path_frame_standing_2.jpg |
| 06a_paper_sim_side_head_height_min_max.jpg | https://arxiv.org/html/2501.05204v1/figures/standing_references/00000.jpg |
| 06b_paper_sim_front_head_yaw_min_max.jpg | https://arxiv.org/html/2501.05204v1/figures/standing_references/00003.jpg |
| 06c_paper_sim_side_head_pitch_min_max.jpg | https://arxiv.org/html/2501.05204v1/figures/standing_references/00002.jpg |
| 06d_paper_sim_front_head_roll_min_max.jpg | https://arxiv.org/html/2501.05204v1/figures/standing_references/00001.jpg |
| 06e_paper_sim_front_torso_height_min_max.jpg | https://arxiv.org/html/2501.05204v1/figures/standing_references/00007.jpg |
| 06f_paper_sim_front_torso_yaw_min_max.jpg | https://arxiv.org/html/2501.05204v1/figures/standing_references/00006.jpg |
| 06g_paper_sim_side_torso_pitch_min_max.jpg | https://arxiv.org/html/2501.05204v1/figures/standing_references/00005.jpg |
| 06h_paper_sim_front_torso_roll_min_max.jpg | https://arxiv.org/html/2501.05204v1/figures/standing_references/00004.jpg |
| 07_paper_standing_controls.jpg | https://arxiv.org/html/2501.05204v1/figures/standing_controls.jpg |
| 10_paper_fig1_three_droids_galaxys_edge.jpg | PDF p.1 (Fig. 1) |
| 11_paper_fig2_green_droid_3quarter_photo.jpg | PDF p.2 (Fig. 2 panel) |
| 12_paper_cad_shell_transparent_3quarter.png | PDF p.2 (Fig. 2 panel, CAD with transparent shell) |
| 13_paper_cad_front_thigh100_vs_thigh195.png | PDF p.2 (Fig. 2 panel, "BD-2 Mechanical Design" thigh-length study) |
| 14_paper_anim_rig_walk_front_3quarter.png | PDF p.2 (Fig. 2 panel, animation rig) |
| 15_paper_anim_rig_walk_side_3quarter.png | PDF p.2 (Fig. 2 panel, animation rig) |
| 18_paper_droid_with_person_scale_a.jpg | PDF p.10 (Fig. 10) |
| 18_paper_droid_with_person_scale_b.jpg | PDF p.10 (Fig. 10) |

## Disney Research
| File | Source |
|---|---|
| 09_disneyresearch_bdx_page.jpg | https://dev-disneyresearch.pantheonsite.io/wp-content/uploads/image-3.jpeg (image on https://la.disneyresearch.com/bdx-droids/) |

## Open Duck Mini (apirrone, Apache-2.0): https://github.com/apirrone/Open_Duck_Mini (branch v2)
| File | Source |
|---|---|
| 20_openduck_v2_photo_1.png | https://github.com/user-attachments/assets/2a407765-70ad-48dd-8a5d-488f82503716 |
| 21_openduck_v2_photo_2.png | https://github.com/user-attachments/assets/3b8fe350-73a9-4c9f-ad29-efc781be7aee |
| 22_openduck_v2_photo_3.png | https://github.com/user-attachments/assets/fd7e5949-1492-4d31-851f-feaa9b695557 |
| 23_openduck_community_collage.png | https://github.com/user-attachments/assets/e240c06e-769f-4c87-b65f-189a442cf1e9 |
| 24_openduck_v2_mod_3d_model.png | https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/print/mods/v2_Jaimes_Mods/3D%20Model.png |
| 25_openduck_v2_mod_render.png | https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/print/mods/v2_Jaimes_Mods/Render.png |
| 27_openduck_v2_cad_render_internals.png | https://hackaday.com/wp-content/uploads/2025/04/Open_Duck_Mini_v2.png (from https://hackaday.com/2025/04/05/disneys-bipedal-bdx-series-droid-gets-the-diy-treatment/) |

## New Atlas: IROS 2023 prototype (https://newatlas.com/robotics/disney-wall-e-robot/)
| File | Source |
|---|---|
| 30_newatlas_iros2023_a.jpg | https://newatlas-brightspot.s3.ap-southeast-2.amazonaws.com/06/b1/00389ab84b41ae163be8385a5a8c/screenshot-2023-10-09-at-2.25.57%20pm.jpg |
| 31_newatlas_iros2023_b.png | https://newatlas-brightspot.s3.ap-southeast-2.amazonaws.com/c0/50/c41b0a4e4f5d8dbc8aefb45ba5d4/screenshot-2023-10-09-at-2.24.21%20pm.png |
| 34_newatlas_iros2023_e.jpg | https://newatlas-brightspot.s3.ap-southeast-2.amazonaws.com/98/cb/fb7b44e24a428fbf422b4dfb45ad/screenshot-2023-10-09-at-2.26.20%20pm.jpg |

## News and fan sites (park versions and GTC 2025 "Blue")
| File | Source image URL | Page |
|---|---|---|
| 40_3dprint_three_droids_galaxys_edge_cast.jpg | https://3dprint.com/wp-content/uploads/2023/10/1697202262687.jpg | https://3dprint.com/304163/disneys-3d-printed-robot-steals-the-show-at-ieee-iros-2023-conference/ |
| 41_3dprint_orange_droid_3quarter_front.jpg | https://3dprint.com/wp-content/uploads/2023/10/1697202251867.jpg | same |
| 42_dtb_three_droids_front_stage.jpg | https://www.disneytouristblog.com/wp-content/uploads/2024/04/bdx-droids-star-wars-galaxys-edge-season-force-disney-disneyland.jpg | https://www.disneytouristblog.com/bdx-droids-coming-to-star-wars-galaxys-edge/ |
| 43_dtb_droids_with_people_scale.jpg | https://www.disneytouristblog.com/wp-content/uploads/2024/04/bdx-droids-star-wars-galaxys-edge-season-force-disney-disneyland-1.jpg | same |
| 44_nvidia_newton_head_closeup_3quarter.jpg | https://samsdisneydiary.com/wp-content/uploads/2025/03/4i-il-xmru.jpg | https://samsdisneydiary.com/2025/03/nvidia-gtc-2025-blue-disney/ |
| 45_nvidia_gtc2025_blue_3quarter_side.jpg | https://samsdisneydiary.com/wp-content/uploads/2025/03/Blue-GTC2025.jpg | same |
| 46_d23_droids_side_walking.jpg | https://i0.wp.com/samsdisneydiary.com/wp-content/uploads/2025/03/Disney-Box-Droids-Fomr-D23-Ultimate-Fan-Event.jpeg?ssl=1 | same |
| 47_techcrunch_gtc2025_jensen_blue_scale.jpg | https://techcrunch.com/wp-content/uploads/2025/03/GettyImages-2205761750.jpg | https://techcrunch.com/2025/03/18/nvidia-and-google-deepmind-will-help-power-disneys-cute-robots/ |
| 50_disneygeek_blue_front_3quarter_high.jpg | https://blog.disneygeek.com/wp-content/uploads/2024/04/wp-17129690357202516462093916422024.jpg | https://blog.disneygeek.com/2024/04/12/pictures-bdx-droids-in-star-wars-galaxys-edge/ |
| 51_disneygeek_blue_side_3quarter_with_person.jpg | https://blog.disneygeek.com/wp-content/uploads/2024/04/wp-17129690356833488295254999014496.jpg | same |
| 52_disneygeek_blue_3quarter_neck_detail.jpg | https://blog.disneygeek.com/wp-content/uploads/2024/04/wp-171296903575737988838095598822.jpg | same |
| 53_disneygeek_head_neck_closeup_front.jpg | https://blog.disneygeek.com/wp-content/uploads/2024/04/wp-17129690358172279432769357852109.jpg | same |
| 54_disneygeek_blue_front_3quarter.jpg | https://blog.disneygeek.com/wp-content/uploads/2024/04/2024_04_12_142453.jpg | same |
| 55_disneygeek_blue_side_leg_detail.jpg | https://blog.disneygeek.com/wp-content/uploads/2024/04/2024_04_12_142358.jpg | same |
| 56_disneygeek_blue_side_view_head_turned.jpg | https://blog.disneygeek.com/wp-content/uploads/2024/04/2024_04_12_140007.jpg | same |
| 57_disneygeek_blue_front_from_above.jpg | https://blog.disneygeek.com/wp-content/uploads/2024/04/2024_04_12_135942.jpg | same |
| 60_ieee_iros2023_prototype_side_profile.jpg | https://spectrum.ieee.org/media-library/image.jpg?id=48631463&width=2400 | https://spectrum.ieee.org/disney-robot |
| 61_ieee_iros2023_prototype_front_with_team.jpg | https://spectrum.ieee.org/media-library/photo-of-five-men-kneeling-around-a-small-robot.jpg?id=48631971&width=2400 | same |
| 62_ieee_iros2023_prototype_front_lowangle.jpg | https://spectrum.ieee.org/media-library/photo-of-a-small-crowd-of-people-surrounding-a-small-robot-and-taking-photos-of-it.jpg?id=48631709&width=2400 | same |
| 63_ieee_iros2023_prototype_3quarter_with_person.jpg | https://spectrum.ieee.org/media-library/photo-of-small-robot-and-a-man.jpg?id=48632157&width=2400 | same |
| 64_laughingplace_wdw_side_3quarter_with_person.jpg | https://www.laughingplace.com/uploads/media/2025/07/16/video-photos-bdx-droids-arrive-at-walt-disney-worlds-star-wars-galaxys-edge-perform-for-guests.jpeg | https://www.laughingplace.com/disney-parks/bdx-droids-star-wars-galaxys-edge-walt-disney-world/ |
| 65_laughingplace_wdw_droids_rear_and_side.jpg | ...perform-for-guests-3.jpeg (same folder) | same |
| 66_laughingplace_wdw_front_with_person.jpg | ...perform-for-guests-4.jpeg (same folder) | same |
| 67_resortsgal_red_front_straight.jpg | https://www.resortsgal.com/wp-content/uploads/bdx-droids-at-star-wars-galaxy-edge.jpg | https://www.resortsgal.com/blog/bdx-droids-at-disney-world/ |
| 68_resortsgal_red_front_with_person_scale.jpg | https://www.resortsgal.com/wp-content/uploads/bdx-droids-disney-world.jpg | same |
| 69_resortsgal_orange_green_front_3quarter.jpg | https://www.resortsgal.com/wp-content/uploads/bdx-droids-hollywood-studios-orange-green.jpg | same |

## BDX-R: full-size open-source replica (https://github.com/BDX-R)
| File | Source |
|---|---|
| 71_bdxr_replica_render_front.png | https://raw.githubusercontent.com/BDX-R/BDX-R.github.io/main/docs/source/_static/bdx_r_front.png |
| 72_bdxr_replica_render_side.png | https://raw.githubusercontent.com/BDX-R/BDX-R.github.io/main/docs/source/_static/bdx_r_side.png |
| 74_bdxr_physical_prototype.png | https://github.com/user-attachments/assets/4f65d9e9-85ad-497f-b687-10c54377d0f2 (BDX-R-IsaacLab README) |

Not downloaded (not an image, 95 MB): the full BDX-R STEP assembly, **`BDX-R V1.step`**, MIT license, at https://github.com/BDX-R/BDX-R-CAD. It can be imported straight into SolidWorks.
