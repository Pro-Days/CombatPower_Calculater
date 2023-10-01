import os
import sys
import json
import requests
import urllib.request
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QIcon, QPixmap


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path("resource//main.ui")
form_class = uic.loadUiType(form)[0]


class MainWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(1280, 720)
        self.setWindowTitle("데이즈 한월RPG 전투력 계산기 v1.0.0")
        self.setWindowIcon(QIcon(resource_path("resource//icon.png")))
        self.add_stuff()
        self.dataload()
        self.setting()
        self.calc()
        self.load_job()

    def add_stuff(self):  # 초기세팅
        self.resize(1280, 720)
        self.centralwidget.setLayout(QtWidgets.QVBoxLayout(self.centralwidget))
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.centralwidget.layout().addWidget(scroll_area)
        scroll_area.setWidget(self.frame_main)
        self.frame_main.setMinimumSize(3500, 1500)  # 크기변경

    def setting(self):  # input 변경시 계산
        input_list = (
            self.input_level,
            self.input_atk,
            self.input_def,
            self.input_hp,
            self.input_crit_chance,
            self.input_crit_dmg,
            self.input_dodge,
            self.input_hit,
            self.input_move_speed,
            self.input_stat,
            self.input_natural_recovery,
            self.input_potion_recovery,
            self.input_cooltime_reduce,
            self.input_atk_speed,
            self.input_luck,
            self.input_steal,
            self.input_exp,
            self.input_boss_dmg,
            self.input_additional_dmg,
            self.input_dmg_a,
            self.input_dmg_b,
            self.input_sim_level,
            self.input_sim_atk,
            self.input_sim_def,
            self.input_sim_hp,
            self.input_sim_crit_chance,
            self.input_sim_crit_dmg,
            self.input_sim_dodge,
            self.input_sim_hit,
            self.input_sim_move_speed,
            self.input_sim_stat,
            self.input_sim_natural_recovery,
            self.input_sim_potion_recovery,
            self.input_sim_cooltime_reduce,
            self.input_sim_atk_speed,
            self.input_sim_luck,
            self.input_sim_steal,
            self.input_sim_exp,
            self.input_sim_boss_dmg,
            self.input_sim_additional_dmg,
        )
        for i in input_list:
            i.textChanged.connect(self.calc)
            i.setTabChangesFocus(True)

        self.input_eff_num.textChanged.connect(self.calc)
        self.combobox_calc_a.currentIndexChanged.connect(self.calc)
        self.combobox_calc_b.currentIndexChanged.connect(self.calc)
        self.combobox_pot_1.currentIndexChanged.connect(self.calc)
        self.combobox_pot_2.currentIndexChanged.connect(self.calc)
        self.combobox_pot_3.currentIndexChanged.connect(self.calc)
        self.combobox_job.currentIndexChanged.connect(self.load_job)

        self.button_save.clicked.connect(self.datasave)
        self.button_capture_load.clicked.connect(self.image)
        self.button_capture_save.clicked.connect(self.capture)

    def load_job(self):
        self.JOB = self.combobox_job.currentIndex()

        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(
            resource_path(f"resource//{self.combobox_job.currentText()}.png")
        )
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(41)
        self.image_job.setPixmap(self.qPixmapFileVar)

    def image(self):
        try:
            self.NAME = self.input_name.toPlainText()
            response = requests.get(
                f"https://api.mojang.com/users/profiles/minecraft/{self.NAME}"
            )
            url = f"https://mc-heads.net/body/{response.json()['id']}/342.png"
            image = urllib.request.urlopen(url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(image)
            self.label_capture_profile.setPixmap(pixmap)
        except:
            self.label_capture_profile.clear()

        self.label_capture_name.setPlainText(self.NAME)
        self.label_capture_name.setAlignment(QtCore.Qt.AlignCenter)

        self.label_capture_job.setPlainText(self.combobox_job.currentText())
        self.label_capture_job.setAlignment(QtCore.Qt.AlignCenter)

        self.label_capture_level.setPlainText("LV." + str(self.LEVEL))
        self.label_capture_level.setAlignment(QtCore.Qt.AlignCenter)

        self.label_capture_boss_num.setPlainText(str(int(self.ConvertedStat_Boss)))
        self.label_capture_boss_num.setAlignment(QtCore.Qt.AlignCenter)
        self.label_capture_dmg_num.setPlainText(str(int(self.ConvertedStat_DAMAGE)))
        self.label_capture_dmg_num.setAlignment(QtCore.Qt.AlignCenter)
        self.label_capture_pve_num.setPlainText(str(int(self.ConvertedStat_PVE)))
        self.label_capture_pve_num.setAlignment(QtCore.Qt.AlignCenter)
        self.label_capture_pvp_num.setPlainText(str(int(self.ConvertedStat_PVP)))
        self.label_capture_pvp_num.setAlignment(QtCore.Qt.AlignCenter)

        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(
            resource_path(f"resource//{self.combobox_job.currentText()}.png")
        )
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(41)
        self.image_capture.setPixmap(self.qPixmapFileVar)

    def capture(self):
        frame_pixmap = self.frame_capture.grab()
        filename = f"{self.NAME}님의 전투력.png"
        frame_pixmap.save(filename)
        os.startfile(filename)

    def calc(self):
        self.button_save.setStyleSheet(
            'background-color: rgb(80, 80, 200);font: 600 18pt "맑은 고딕";color: rgb(255, 255, 255);'
        )

        try:
            self.stat_ToInt()
        except Exception as e:
            print("stat_ToInt", e)
            self.stat_DisplayError()
            self.sim_DisplayError()
            self.eff_DisplayError()
            return
        try:
            self.sim_ToInt()
        except Exception as e:
            print("sim_ToInt", e)
            self.sim_DisplayError()
            self.eff_DisplayError()
            return
        try:
            self.eff_ToInt()
        except Exception as e:
            print("eff_ToInt", e)
            self.eff_DisplayError()
            return

        if self.if_inputError():
            print("Input Error")
            self.stat_DisplayError()
            self.sim_DisplayError()
            self.eff_DisplayError()
            return
        else:
            try:
                self.calc_ConvertedStat()
            except Exception as e:
                print("calc_ConvertedStat", e)
                self.stat_DisplayError()
                self.sim_DisplayError()
                self.eff_DisplayError()
                return
            try:
                self.calc_SimulatedConvertedStat()
            except Exception as e:
                print("calc_SimulatedConvertedStat", e)
                self.sim_DisplayError()
                self.eff_DisplayError()
                return
            try:
                self.calc_efficiency()
            except Exception as e:
                self.eff_DisplayError()
                return
            try:
                self.sort_pot_ind()
            except Exception as e:
                print("sort_pot_ind", e)
                return
            try:
                self.sort_pot()
            except Exception as e:
                print("sort_pot", e)
                return

    def stat_ToInt(self):
        self.LEVEL = int(self.input_level.toPlainText())
        self.ATK = int(self.input_atk.toPlainText())
        self.DEF = int(self.input_def.toPlainText())
        self.HP = int(self.input_hp.toPlainText())
        self.CRIT_CHANCE = int(self.input_crit_chance.toPlainText())
        self.CRIT_CHANCE = 100 if self.CRIT_CHANCE > 100 else self.CRIT_CHANCE
        self.CRIT_DMG = int(self.input_crit_dmg.toPlainText())
        self.DODGE = int(self.input_dodge.toPlainText())
        self.DODGE = 100 if self.DODGE > 100 else self.DODGE
        self.HIT = int(self.input_hit.toPlainText())
        self.HIT = 100 if self.HIT > 100 else self.HIT
        self.MOVE_SPEED = int(self.input_move_speed.toPlainText())
        self.STAT = int(self.input_stat.toPlainText())
        self.NATURAL_RECOVERY = int(self.input_natural_recovery.toPlainText())
        self.POTION_RECOVERY = int(self.input_potion_recovery.toPlainText())
        self.COOLTIME_REDUCE = int(self.input_cooltime_reduce.toPlainText())
        self.COOLTIME_REDUCE = 50 if self.COOLTIME_REDUCE > 50 else self.COOLTIME_REDUCE
        self.ATK_SPEED = int(self.input_atk_speed.toPlainText())
        self.LUCK = int(self.input_luck.toPlainText())
        self.STEAL = int(self.input_steal.toPlainText())
        self.EXP = int(self.input_exp.toPlainText())
        self.BOSS_DMG = int(self.input_boss_dmg.toPlainText())
        self.ADDITIONAL_DMG = int(self.input_additional_dmg.toPlainText())
        self.DMG_A = int(self.input_dmg_a.toPlainText())
        self.DMG_B = int(self.input_dmg_b.toPlainText())

    def sim_ToInt(self):
        self.SIM_LEVEL = int(self.input_sim_level.toPlainText())
        self.SIM_ATK = int(self.input_sim_atk.toPlainText())
        self.SIM_DEF = int(self.input_sim_def.toPlainText())
        self.SIM_HP = int(self.input_sim_hp.toPlainText())
        self.SIM_CRIT_CHANCE = int(self.input_sim_crit_chance.toPlainText())
        self.SIM_CRIT_DMG = int(self.input_sim_crit_dmg.toPlainText())
        self.SIM_DODGE = int(self.input_sim_dodge.toPlainText())
        self.SIM_HIT = int(self.input_sim_hit.toPlainText())
        self.SIM_MOVE_SPEED = int(self.input_sim_move_speed.toPlainText())
        self.SIM_STAT = int(self.input_sim_stat.toPlainText())
        self.SIM_NATURAL_RECOVERY = int(self.input_sim_natural_recovery.toPlainText())
        self.SIM_POTION_RECOVERY = int(self.input_sim_potion_recovery.toPlainText())
        self.SIM_COOLTIME_REDUCE = int(self.input_sim_cooltime_reduce.toPlainText())
        self.SIM_ATK_SPEED = int(self.input_sim_atk_speed.toPlainText())
        self.SIM_LUCK = int(self.input_sim_luck.toPlainText())
        self.SIM_STEAL = int(self.input_sim_steal.toPlainText())
        self.SIM_EXP = int(self.input_sim_exp.toPlainText())
        self.SIM_BOSS_DMG = int(self.input_sim_boss_dmg.toPlainText())
        self.SIM_ADDITIONAL_DMG = int(self.input_sim_additional_dmg.toPlainText())

    def eff_ToInt(self):
        self.eff_num = int(self.input_eff_num.toPlainText())

    def if_inputError(self):
        if self.LEVEL > 200:  # 레벨 200초과면 오류
            return False
        if self.CRIT_CHANCE > 200:  # 치확 100% 초과면 100%로 고정
            self.CRIT_CHANCE = 200

        # print(
        #     int(
        #         (self.ATK * 1.08 + self.ATK * self.STAT * 0.0032)
        #         * (1 + self.ADDITIONAL_DMG * 0.01)
        #     ),
        #     int(
        #         int(
        #             (self.ATK * 1.08 + self.ATK * self.STAT * 0.0032)
        #             * (1 + self.ADDITIONAL_DMG * 0.01)
        #         )
        #         * 0.82
        #     ),
        # )
        if self.DMG_B != int(
            (self.ATK * 1.08 + self.ATK * self.STAT * 0.0032)
            * (1 + self.ADDITIONAL_DMG * 0.01)
        ):  # 데미지(뒤) 검산 (수식 변경 필요)
            return True
        elif self.DMG_A != int(
            self.DMG_B * 0.82
        ):  # 데미지(앞) 검산 (수식 변경 필요) / 크가에서는 0.82 -> 버림
            return True
        else:
            return False

    def stat_DisplayError(self):
        self.label_stat_boss_num.setPlainText("오류")
        self.label_stat_damage_num.setPlainText("오류")
        self.label_stat_pve_num.setPlainText("오류")
        self.label_stat_pvp_num.setPlainText("오류")
        self.label_stat_boss_num.setAlignment(QtCore.Qt.AlignCenter)
        self.label_stat_damage_num.setAlignment(QtCore.Qt.AlignCenter)
        self.label_stat_pve_num.setAlignment(QtCore.Qt.AlignCenter)
        self.label_stat_pvp_num.setAlignment(QtCore.Qt.AlignCenter)

    def sim_DisplayError(self):
        self.label_sim_pred_boss_num.setPlainText("오류")
        self.label_sim_pred_damage_num.setPlainText("오류")
        self.label_sim_pred_pve_num.setPlainText("오류")
        self.label_sim_pred_pvp_num.setPlainText("오류")
        self.label_sim_pred_boss_num.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sim_pred_damage_num.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sim_pred_pve_num.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sim_pred_pvp_num.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sim_pred_deal_num.setPlainText("오류")
        self.label_sim_pred_deal_num.setAlignment(QtCore.Qt.AlignCenter)

    def eff_DisplayError(self):
        self.label_eff_boss_num.setPlainText("오류")
        self.label_eff_damage_num.setPlainText("오류")
        self.label_eff_pve_num.setPlainText("오류")
        self.label_eff_pvp_num.setPlainText("오류")
        self.label_eff_boss_num.setAlignment(QtCore.Qt.AlignCenter)
        self.label_eff_damage_num.setAlignment(QtCore.Qt.AlignCenter)
        self.label_eff_pve_num.setAlignment(QtCore.Qt.AlignCenter)
        self.label_eff_pvp_num.setAlignment(QtCore.Qt.AlignCenter)

    def calc_BossStat(
        self,
        LEVEL,
        ATK,
        STAT,
        HP,
        DEF,
        NATURAL_RECOVERY,
        POTION_RECOVERY,
        DODGE,
        CRIT_CHANCE,
        CRIT_DMG,
        COOLTIME_REDUCE,
        ATK_SPEED,
        ADDITIONAL_DMG,
        BOSS_DMG,
    ):
        if LEVEL <= 100:  # 포션 회복량 -> 레벨에 따라 수정해야함
            POTION = 100
        else:
            POTION = 300

        return (
            (ATK * 1.08 + ATK * STAT * 0.0032)
            * (1 + ADDITIONAL_DMG * 0.01)
            * (1 + CRIT_CHANCE * CRIT_DMG * 0.000025)
            * HP
            * (1 + DEF * 0.015)
            * (
                (HP * NATURAL_RECOVERY * 0.004 / POTION + 0.01 * POTION_RECOVERY) * 0.1
                + 1
            )
            * (1 + (COOLTIME_REDUCE * 0.01) / (1 - COOLTIME_REDUCE * 0.01) * 0.95)
            * (1 + (ATK_SPEED * 0.01) / (1 - ATK_SPEED * 0.01) * 0.05)
            * (1 + DODGE * 0.00125)  # 1% -> 0.5%
            * (1 + BOSS_DMG * 0.01)
            * 0.001
        )

    def calc_DamageStat(
        self,
        ATK,
        STAT,
        CRIT_CHANCE,
        CRIT_DMG,
        COOLTIME_REDUCE,
        ATK_SPEED,
        ADDITIONAL_DMG,
        BOSS_DMG,
    ):
        return (
            (ATK * 1.08 + ATK * STAT * 0.0032)
            * (1 + ADDITIONAL_DMG * 0.01)
            * (1 + CRIT_CHANCE * CRIT_DMG * 0.000025)
            * (1 + (COOLTIME_REDUCE * 0.01) / (1 - COOLTIME_REDUCE * 0.01) * 0.95)
            * (1 + (ATK_SPEED * 0.01) / (1 - ATK_SPEED * 0.01) * 0.05)
            * (1 + BOSS_DMG * 0.01)
            * 14.5
        )

    def calc_PVEStat(
        self,
        LEVEL,
        ATK,
        STAT,
        HP,
        DEF,
        NATURAL_RECOVERY,
        POTION_RECOVERY,
        DODGE,
        CRIT_CHANCE,
        CRIT_DMG,
        COOLTIME_REDUCE,
        ATK_SPEED,
        ADDITIONAL_DMG,
        LUCK,
        STEAL,
        EXP,
        BOSS_DMG,
    ):
        if LEVEL <= 100:  # 포션 회복량 -> 레벨에 따라 수정해야함
            POTION = 100
        else:
            POTION = 300

        return (
            (ATK * 1.08 + ATK * STAT * 0.0032)
            * (1 + ADDITIONAL_DMG * 0.01)
            * (1 + CRIT_CHANCE * CRIT_DMG * 0.000025)
            * HP
            * (1 + DEF * 0.0125)
            * (
                (HP * NATURAL_RECOVERY * 0.004 / POTION + 0.01 * POTION_RECOVERY) * 0.1
                + 1
            )
            * (1 + (COOLTIME_REDUCE * 0.01) / (1 - COOLTIME_REDUCE * 0.01) * 0.95)
            * (1 + (ATK_SPEED * 0.01) / (1 - ATK_SPEED * 0.01) * 0.05)
            * (1 + DODGE * 0.000625)
            * (1 + LUCK * 0.002)
            * (1 + STEAL * 0.004)
            * (1 + EXP * 0.02)
            * (1 + BOSS_DMG * 0.01)
            * 0.0011
        )

    def calc_PVPStat(
        self,
        ATK,
        STAT,
        HP,
        DEF,
        NATURAL_RECOVERY,
        DODGE,
        CRIT_CHANCE,
        CRIT_DMG,
        COOLTIME_REDUCE,
        ATK_SPEED,
        ADDITIONAL_DMG,
        HIT,
        MOVE_SPEED,
    ):
        return (
            (ATK * 1.08 + ATK * STAT * 0.0032)
            * (1 + ADDITIONAL_DMG * 0.01)
            * (1 + CRIT_CHANCE * CRIT_DMG * 0.000025)
            * HP
            * (1 + DEF * 0.0175)
            * (1 + NATURAL_RECOVERY * 0.02 * 0.1)
            * (1 + (COOLTIME_REDUCE * 0.01) / (1 - COOLTIME_REDUCE * 0.01) * 0.95)
            * (1 + (ATK_SPEED * 0.01) / (1 - ATK_SPEED * 0.01) * 0.05)
            * (1 + MOVE_SPEED * 0.04)
            * (1 + HIT * 0.0009375)  # 1% -> 0.75%
            * (1 + DODGE * 0.0025)  # 1% -> 1%
            * 0.00055
        )

    def calc_SimulatedConvertedStat(self):
        LEVEL = self.LEVEL + self.SIM_LEVEL
        LEVEL = 200 if LEVEL > 200 else LEVEL
        ATK = self.ATK + self.SIM_ATK
        DEF = self.DEF + self.SIM_DEF
        HP = self.HP + self.SIM_HP
        HP += 10 * (LEVEL - self.LEVEL)
        CRIT_CHANCE = self.CRIT_CHANCE + self.SIM_CRIT_CHANCE
        CRIT_CHANCE = 200 if CRIT_CHANCE > 200 else CRIT_CHANCE
        CRIT_DMG = self.CRIT_DMG + self.SIM_CRIT_DMG
        DODGE = self.DODGE + self.SIM_DODGE
        DODGE = 400 if DODGE > 400 else DODGE
        HIT = self.HIT + self.SIM_HIT
        HIT = 800 if HIT > 800 else HIT
        MOVE_SPEED = self.MOVE_SPEED + self.SIM_MOVE_SPEED
        STAT = self.STAT + self.SIM_STAT
        NATURAL_RECOVERY = self.NATURAL_RECOVERY + self.SIM_NATURAL_RECOVERY
        POTION_RECOVERY = self.POTION_RECOVERY + self.SIM_POTION_RECOVERY
        COOLTIME_REDUCE = self.COOLTIME_REDUCE + self.SIM_COOLTIME_REDUCE
        COOLTIME_REDUCE = 50 if COOLTIME_REDUCE > 50 else COOLTIME_REDUCE
        ATK_SPEED = self.ATK_SPEED + self.SIM_ATK_SPEED
        LUCK = self.LUCK + self.SIM_LUCK
        STEAL = self.STEAL + self.SIM_STEAL
        EXP = self.EXP + self.SIM_EXP
        BOSS_DMG = self.BOSS_DMG + self.SIM_BOSS_DMG
        ADDITIONAL_DMG = self.ADDITIONAL_DMG + self.SIM_ADDITIONAL_DMG

        SimConvertedStat_Boss = int(
            self.calc_BossStat(
                LEVEL,
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                POTION_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                BOSS_DMG,
            )
        )
        self.label_sim_pred_boss_num.setPlainText(str(SimConvertedStat_Boss))
        self.label_sim_pred_boss_num.setAlignment(QtCore.Qt.AlignCenter)

        SimConvertedStat_DAMAGE = int(
            self.calc_DamageStat(
                ATK,
                STAT,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                BOSS_DMG,
            )
        )
        self.label_sim_pred_damage_num.setPlainText(str(SimConvertedStat_DAMAGE))
        self.label_sim_pred_damage_num.setAlignment(QtCore.Qt.AlignCenter)

        SimConvertedStat_PVE = int(
            self.calc_PVEStat(
                LEVEL,
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                POTION_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                LUCK,
                STEAL,
                EXP,
                BOSS_DMG,
            )
        )
        self.label_sim_pred_pve_num.setPlainText(str(SimConvertedStat_PVE))
        self.label_sim_pred_pve_num.setAlignment(QtCore.Qt.AlignCenter)

        SimConvertedStat_PVP = int(
            self.calc_PVPStat(
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                HIT,
                MOVE_SPEED,
            )
        )
        self.label_sim_pred_pvp_num.setPlainText(str(SimConvertedStat_PVP))
        self.label_sim_pred_pvp_num.setAlignment(QtCore.Qt.AlignCenter)

        SimDamageIncrease = round(
            (
                SimConvertedStat_DAMAGE / int(self.label_stat_damage_num.toPlainText())
                - 1
            )
            * 100,
            2,
        )
        self.label_sim_pred_deal_num.setPlainText(str(SimDamageIncrease) + "%")
        self.label_sim_pred_deal_num.setAlignment(QtCore.Qt.AlignCenter)

        dmg_a = int((ATK * 1.08 + ATK * STAT * 0.0032) * (1 + ADDITIONAL_DMG * 0.01))
        self.label_sim_pred_dmg_a_num.setPlainText(str(dmg_a))
        self.label_sim_pred_dmg_a_num.setAlignment(QtCore.Qt.AlignCenter)
        dmg_b = int(dmg_a * 0.82)
        self.label_sim_pred_dmg_b_num.setPlainText(str(dmg_b))
        self.label_sim_pred_dmg_b_num.setAlignment(QtCore.Qt.AlignCenter)

    def calc_ConvertedStat(self):
        self.ConvertedStat_Boss = self.calc_BossStat(
            self.LEVEL,
            self.ATK,
            self.STAT,
            self.HP,
            self.DEF,
            self.NATURAL_RECOVERY,
            self.POTION_RECOVERY,
            self.DODGE,
            self.CRIT_CHANCE,
            self.CRIT_DMG,
            self.COOLTIME_REDUCE,
            self.ATK_SPEED,
            self.ADDITIONAL_DMG,
            self.BOSS_DMG,
        )
        self.label_stat_boss_num.setPlainText(str(int(self.ConvertedStat_Boss)))
        self.label_stat_boss_num.setAlignment(QtCore.Qt.AlignCenter)
        # print("BOSS")

        self.ConvertedStat_DAMAGE = self.calc_DamageStat(
            self.ATK,
            self.STAT,
            self.CRIT_CHANCE,
            self.CRIT_DMG,
            self.COOLTIME_REDUCE,
            self.ATK_SPEED,
            self.ADDITIONAL_DMG,
            self.BOSS_DMG,
        )
        self.label_stat_damage_num.setPlainText(str(int(self.ConvertedStat_DAMAGE)))
        self.label_stat_damage_num.setAlignment(QtCore.Qt.AlignCenter)
        # print("NORMAL")

        self.ConvertedStat_PVE = self.calc_PVEStat(
            self.LEVEL,
            self.ATK,
            self.STAT,
            self.HP,
            self.DEF,
            self.NATURAL_RECOVERY,
            self.POTION_RECOVERY,
            self.DODGE,
            self.CRIT_CHANCE,
            self.CRIT_DMG,
            self.COOLTIME_REDUCE,
            self.ATK_SPEED,
            self.ADDITIONAL_DMG,
            self.LUCK,
            self.STEAL,
            self.EXP,
            self.BOSS_DMG,
        )
        self.label_stat_pve_num.setPlainText(str(int(self.ConvertedStat_PVE)))
        self.label_stat_pve_num.setAlignment(QtCore.Qt.AlignCenter)
        # print("PVE")

        self.ConvertedStat_PVP = self.calc_PVPStat(
            self.ATK,
            self.STAT,
            self.HP,
            self.DEF,
            self.NATURAL_RECOVERY,
            self.DODGE,
            self.CRIT_CHANCE,
            self.CRIT_DMG,
            self.COOLTIME_REDUCE,
            self.ATK_SPEED,
            self.ADDITIONAL_DMG,
            self.HIT,
            self.MOVE_SPEED,
        )
        self.label_stat_pvp_num.setPlainText(str(int(self.ConvertedStat_PVP)))
        self.label_stat_pvp_num.setAlignment(QtCore.Qt.AlignCenter)
        # print("PVP")

    def calc_efficiency(self):
        compare_TypeA = self.combobox_calc_a.currentText()
        compare_TypeB = self.combobox_calc_b.currentText()

        LEVEL = self.LEVEL
        ATK = self.ATK
        DEF = self.DEF
        HP = self.HP
        CRIT_CHANCE = self.CRIT_CHANCE
        CRIT_DMG = self.CRIT_DMG
        DODGE = self.DODGE
        HIT = self.HIT
        MOVE_SPEED = self.MOVE_SPEED
        STAT = self.STAT
        NATURAL_RECOVERY = self.NATURAL_RECOVERY
        POTION_RECOVERY = self.POTION_RECOVERY
        COOLTIME_REDUCE = self.COOLTIME_REDUCE
        ATK_SPEED = self.ATK_SPEED
        LUCK = self.LUCK
        STEAL = self.STEAL
        EXP = self.EXP
        BOSS_DMG = self.BOSS_DMG
        ADDITIONAL_DMG = self.ADDITIONAL_DMG

        if compare_TypeA == "레벨":
            LEVEL = self.LEVEL + self.eff_num
            LEVEL = 200 if LEVEL > 200 else LEVEL
            HP += 10 * (LEVEL - self.LEVEL)
            calc_list1 = ["BOSS", "PVE"]
        elif compare_TypeA == "공격력":
            ATK = self.ATK + self.eff_num
            calc_list1 = ["BOSS", "DAMAGE", "PVE", "PVP"]
        elif compare_TypeA == "방어력":
            DEF = self.DEF + self.eff_num
            calc_list1 = ["BOSS", "PVE", "PVP"]
        elif compare_TypeA == "체력":
            HP = self.HP + self.eff_num
            calc_list1 = ["BOSS", "PVE", "PVP"]
        elif compare_TypeA == "치명타확률":
            CRIT_CHANCE = self.CRIT_CHANCE + self.eff_num
            CRIT_CHANCE = 200 if CRIT_CHANCE > 200 else CRIT_CHANCE
            calc_list1 = ["BOSS", "DAMAGE", "PVE", "PVP"]
        elif compare_TypeA == "치명타데미지":
            CRIT_DMG = self.CRIT_DMG + self.eff_num
            calc_list1 = ["BOSS", "DAMAGE", "PVE", "PVP"]
        elif compare_TypeA == "회피율":
            DODGE = self.DODGE + self.eff_num
            DODGE = 400 if DODGE > 400 else DODGE
            calc_list1 = ["BOSS", "PVE", "PVP"]
        elif compare_TypeA == "명중률":
            HIT = self.HIT + self.eff_num
            HIT = 800 if HIT > 800 else HIT
            calc_list1 = ["PVP"]
        elif compare_TypeA == "이동속도":
            MOVE_SPEED = self.MOVE_SPEED + self.eff_num
            calc_list1 = ["PVP"]
        elif compare_TypeA == "주스텟":
            STAT = self.STAT + self.eff_num
            calc_list1 = ["BOSS", "DAMAGE", "PVE", "PVP"]
        elif compare_TypeA == "자연회복력":
            NATURAL_RECOVERY = self.NATURAL_RECOVERY + self.eff_num
            calc_list1 = ["BOSS", "PVE", "PVP"]
        elif compare_TypeA == "포션회복력":
            POTION_RECOVERY = self.POTION_RECOVERY + self.eff_num
            calc_list1 = ["BOSS", "PVE"]
        elif compare_TypeA == "스킬시간감소":
            COOLTIME_REDUCE = self.COOLTIME_REDUCE + self.eff_num
            COOLTIME_REDUCE = 50 if COOLTIME_REDUCE > 50 else COOLTIME_REDUCE
            calc_list1 = ["BOSS", "DAMAGE", "PVE", "PVP"]
        elif compare_TypeA == "평타속도":
            ATK_SPEED = self.ATK_SPEED + self.eff_num
            calc_list1 = ["BOSS", "DAMAGE", "PVE", "PVP"]
        elif compare_TypeA == "운":
            LUCK = self.LUCK + self.eff_num
            calc_list1 = ["DAMAGE", "PVE"]
        elif compare_TypeA == "도적질":
            STEAL = self.STEAL + self.eff_num
            calc_list1 = ["PVE"]
        elif compare_TypeA == "경험치추가":
            EXP = self.EXP + self.eff_num
            calc_list1 = ["PVE"]
        elif compare_TypeA == "보스데미지":
            BOSS_DMG = self.BOSS_DMG + self.eff_num
            calc_list1 = ["BOSS", "PVE"]
        elif compare_TypeA == "추가데미지":
            ADDITIONAL_DMG = self.ADDITIONAL_DMG + self.eff_num
            calc_list1 = ["BOSS", "DAMAGE", "PVE", "PVP"]

        if compare_TypeB == "레벨":
            calc_list2 = ["BOSS", "PVE"]
        elif compare_TypeB == "공격력":
            calc_list2 = ["BOSS", "DAMAGE", "PVE", "PVP"]
        elif compare_TypeB == "방어력":
            calc_list2 = ["BOSS", "PVE", "PVP"]
        elif compare_TypeB == "체력":
            calc_list2 = ["BOSS", "PVE", "PVP"]
        elif compare_TypeB == "치명타확률":
            calc_list2 = ["BOSS", "DAMAGE", "PVE", "PVP"]
        elif compare_TypeB == "치명타데미지":
            calc_list2 = ["BOSS", "DAMAGE", "PVE", "PVP"]
        elif compare_TypeB == "회피율":
            calc_list2 = ["BOSS", "PVE", "PVP"]
        elif compare_TypeB == "명중률":
            calc_list2 = ["PVP"]
        elif compare_TypeB == "이동속도":
            calc_list2 = ["PVP"]
        elif compare_TypeB == "주스텟":
            calc_list2 = ["BOSS", "DAMAGE", "PVE", "PVP"]
        elif compare_TypeB == "자연회복력":
            calc_list2 = ["BOSS", "PVE", "PVP"]
        elif compare_TypeB == "포션회복력":
            calc_list2 = ["BOSS", "PVE"]
        elif compare_TypeB == "스킬시간감소":
            calc_list2 = ["BOSS", "DAMAGE", "PVE", "PVP"]
        elif compare_TypeB == "평타속도":
            calc_list2 = ["BOSS", "DAMAGE", "PVE", "PVP"]
        elif compare_TypeB == "운":
            calc_list2 = ["PVE"]
        elif compare_TypeB == "도적질":
            calc_list2 = ["PVE"]
        elif compare_TypeB == "경험치추가":
            calc_list2 = ["PVE"]
        elif compare_TypeB == "보스데미지":
            calc_list2 = ["BOSS", "PVE"]
        elif compare_TypeB == "추가데미지":
            calc_list2 = ["BOSS", "DAMAGE", "PVE", "PVP"]

        # print(compare_TypeA + str(self.eff_num) + compare_TypeB)

        if self.eff_num == 0:
            BOSS_ratio = 0
        elif "BOSS" in (calc_list1 and calc_list2):
            Boss_Goal = self.calc_BossStat(
                LEVEL,
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                POTION_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                BOSS_DMG,
            )
            BOSS_ratio = self.return_ratio(100, 0, Boss_Goal, "BOSS", compare_TypeB)
            BOSS_ratio = round(BOSS_ratio, 4)
        else:
            BOSS_ratio = 0
        self.label_eff_boss_num.setPlainText(str(BOSS_ratio))
        self.label_eff_boss_num.setAlignment(QtCore.Qt.AlignCenter)
        # print("BOSS:" + str(BOSS_ratio))

        if self.eff_num == 0:
            DAMAGE_ratio = 0
        elif "DAMAGE" in (calc_list1 and calc_list2):
            Damage_Goal = self.calc_DamageStat(
                ATK,
                STAT,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                BOSS_DMG,
            )
            DAMAGE_ratio = self.return_ratio(
                100, 0, Damage_Goal, "DAMAGE", compare_TypeB
            )
            DAMAGE_ratio = round(DAMAGE_ratio, 4)
        else:
            DAMAGE_ratio = 0
        self.label_eff_damage_num.setPlainText(str(DAMAGE_ratio))
        self.label_eff_damage_num.setAlignment(QtCore.Qt.AlignCenter)
        # print("DAMAGE:" + str(DAMAGE_ratio))

        if self.eff_num == 0:
            PVE_ratio = 0
        elif "PVE" in (calc_list1 and calc_list2):
            PVE_Goal = self.calc_PVEStat(
                LEVEL,
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                POTION_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                LUCK,
                STEAL,
                EXP,
                BOSS_DMG,
            )
            PVE_ratio = self.return_ratio(100, 0, PVE_Goal, "PVE", compare_TypeB)
            PVE_ratio = round(PVE_ratio, 4)
        else:
            PVE_ratio = 0
        self.label_eff_pve_num.setPlainText(str(PVE_ratio))
        self.label_eff_pve_num.setAlignment(QtCore.Qt.AlignCenter)
        # print("PVE:" + str(PVE_ratio))

        if self.eff_num == 0:
            PVP_ratio = 0
        elif "PVP" in (calc_list1 and calc_list2):
            PVP_Goal = self.calc_PVPStat(
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                HIT,
                MOVE_SPEED,
            )
            PVP_ratio = self.return_ratio(100, 0, PVP_Goal, "PVP", compare_TypeB)
            PVP_ratio = round(PVP_ratio, 4)
        else:
            PVP_ratio = 0
        self.label_eff_pvp_num.setPlainText(str(PVP_ratio))
        self.label_eff_pvp_num.setAlignment(QtCore.Qt.AlignCenter)
        # print("PVP:" + str(PVP_ratio))

    def return_ratio(self, max, min, goal, type, objective_stat, num=1):
        value = (max + min) * 0.5

        LEVEL = self.LEVEL
        ATK = self.ATK
        DEF = self.DEF
        HP = self.HP
        CRIT_CHANCE = self.CRIT_CHANCE
        CRIT_DMG = self.CRIT_DMG
        DODGE = self.DODGE
        HIT = self.HIT
        MOVE_SPEED = self.MOVE_SPEED
        STAT = self.STAT
        NATURAL_RECOVERY = self.NATURAL_RECOVERY
        POTION_RECOVERY = self.POTION_RECOVERY
        COOLTIME_REDUCE = self.COOLTIME_REDUCE
        ATK_SPEED = self.ATK_SPEED
        LUCK = self.LUCK
        STEAL = self.STEAL
        EXP = self.EXP
        BOSS_DMG = self.BOSS_DMG
        ADDITIONAL_DMG = self.ADDITIONAL_DMG

        if objective_stat == "레벨":
            LEVEL = self.LEVEL + value
            if LEVEL > 200:
                return self.return_ratio(
                    value, min, goal, type, objective_stat, num + 1
                )
            else:
                HP += 10 * value
        elif objective_stat == "공격력":
            ATK = self.ATK + value
        elif objective_stat == "방어력":
            DEF = self.DEF + value
        elif objective_stat == "체력":
            HP = self.HP + value
        elif objective_stat == "치명타확률":
            CRIT_CHANCE = self.CRIT_CHANCE + value
            if CRIT_CHANCE > 200:
                return self.return_ratio(
                    value, min, goal, type, objective_stat, num + 1
                )
        elif objective_stat == "치명타데미지":
            CRIT_DMG = self.CRIT_DMG + value
        elif objective_stat == "회피율":
            DODGE = self.DODGE + value
            if DODGE > 400:
                return self.return_ratio(
                    value, min, goal, type, objective_stat, num + 1
                )
        elif objective_stat == "명중률":
            HIT = self.HIT + value
            if HIT > 800:
                return self.return_ratio(
                    value, min, goal, type, objective_stat, num + 1
                )
        elif objective_stat == "이동속도":
            MOVE_SPEED = self.MOVE_SPEED + value
        elif objective_stat == "주스텟":
            STAT = self.STAT + value
        elif objective_stat == "자연회복력":
            NATURAL_RECOVERY = self.NATURAL_RECOVERY + value
        elif objective_stat == "포션회복력":
            POTION_RECOVERY = self.POTION_RECOVERY + value
        elif objective_stat == "스킬시간감소":
            COOLTIME_REDUCE = self.COOLTIME_REDUCE + value
            if COOLTIME_REDUCE > 50:
                return self.return_ratio(
                    value, min, goal, type, objective_stat, num + 1
                )
        elif objective_stat == "평타속도":
            ATK_SPEED = self.ATK_SPEED + value
        elif objective_stat == "운":
            LUCK = self.LUCK + value
        elif objective_stat == "도적질":
            STEAL = self.STEAL + value
        elif objective_stat == "경험치추가":
            EXP = self.EXP + value
        elif objective_stat == "보스데미지":
            BOSS_DMG = self.BOSS_DMG + value
        elif objective_stat == "추가데미지":
            ADDITIONAL_DMG = self.ADDITIONAL_DMG + value

        if "BOSS" == type:
            result = self.calc_BossStat(
                LEVEL,
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                POTION_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                BOSS_DMG,
            )
        elif "DAMAGE" == type:
            result = self.calc_DamageStat(
                ATK,
                STAT,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                BOSS_DMG,
            )
        elif "PVE" == type:
            result = self.calc_PVEStat(
                LEVEL,
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                POTION_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                LUCK,
                STEAL,
                EXP,
                BOSS_DMG,
            )
        else:
            result = self.calc_PVPStat(
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                HIT,
                MOVE_SPEED,
            )
        if num <= 50:
            # print(value)
            if result > goal:
                return self.return_ratio(
                    value, min, goal, type, objective_stat, num + 1
                )
            elif result < goal:
                return self.return_ratio(
                    max, value, goal, type, objective_stat, num + 1
                )
            else:
                # print("else", str(result), str(goal))
                return value
        else:
            return value

    def calc_pot_ind(self, opt, value):
        LEVEL = self.LEVEL
        ATK = self.ATK
        DEF = self.DEF
        HP = self.HP
        CRIT_CHANCE = self.CRIT_CHANCE
        CRIT_DMG = self.CRIT_DMG
        DODGE = self.DODGE
        HIT = self.HIT
        MOVE_SPEED = self.MOVE_SPEED
        STAT = self.STAT
        NATURAL_RECOVERY = self.NATURAL_RECOVERY
        POTION_RECOVERY = self.POTION_RECOVERY
        COOLTIME_REDUCE = self.COOLTIME_REDUCE
        ATK_SPEED = self.ATK_SPEED
        LUCK = self.LUCK
        STEAL = self.STEAL
        EXP = self.EXP
        BOSS_DMG = self.BOSS_DMG
        ADDITIONAL_DMG = self.ADDITIONAL_DMG

        if opt == "공격력":
            ATK = self.ATK + value
        elif opt == "방어력":
            DEF = self.DEF + value
        elif opt == "치명타확률":
            CRIT_CHANCE = self.CRIT_CHANCE + value
            CRIT_CHANCE = 200 if CRIT_CHANCE > 200 else CRIT_CHANCE
        elif opt == "치명타데미지":
            CRIT_DMG = self.CRIT_DMG + value
        elif opt == "회피율":
            DODGE = self.DODGE + value
            DODGE = 400 if DODGE > 400 else DODGE
        elif opt == "명중률":
            HIT = self.HIT + value
            HIT = 800 if HIT > 800 else HIT
        elif opt == "스텟":
            STAT = self.STAT + value
        elif opt == "자연회복력":
            NATURAL_RECOVERY = self.NATURAL_RECOVERY + value
        elif opt == "포션회복력":
            POTION_RECOVERY = self.POTION_RECOVERY + value
        elif opt == "스킬시간감소":
            COOLTIME_REDUCE = self.COOLTIME_REDUCE + value
            COOLTIME_REDUCE = 50 if COOLTIME_REDUCE > 50 else COOLTIME_REDUCE
        elif opt == "평타속도":
            ATK_SPEED = self.ATK_SPEED + value
        elif opt == "운":
            LUCK = self.LUCK + value
        elif opt == "도적질":
            STEAL = self.STEAL + value
        elif opt == "보스데미지":
            BOSS_DMG = self.BOSS_DMG + value

        result_boss = (
            self.calc_BossStat(
                LEVEL,
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                POTION_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                BOSS_DMG,
            )
            / self.ConvertedStat_Boss
            - 1
        ) * 100
        result_dmg = (
            self.calc_DamageStat(
                ATK,
                STAT,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                BOSS_DMG,
            )
            / self.ConvertedStat_DAMAGE
            - 1
        ) * 100
        result_pve = (
            self.calc_PVEStat(
                LEVEL,
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                POTION_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                LUCK,
                STEAL,
                EXP,
                BOSS_DMG,
            )
            / self.ConvertedStat_PVE
            - 1
        ) * 100
        result_pvp = (
            self.calc_PVPStat(
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                HIT,
                MOVE_SPEED,
            )
            / self.ConvertedStat_PVP
            - 1
        ) * 100

        return (result_boss, result_dmg, result_pve, result_pvp)

    def sort_pot_ind(self):
        labels_opt = [
            [
                self.label_rank_opt_boss_1,
                self.label_rank_opt_boss_2,
                self.label_rank_opt_boss_3,
                self.label_rank_opt_boss_4,
                self.label_rank_opt_boss_5,
                self.label_rank_opt_boss_6,
                self.label_rank_opt_boss_7,
                self.label_rank_opt_boss_8,
                self.label_rank_opt_boss_9,
                self.label_rank_opt_boss_10,
                self.label_rank_opt_boss_11,
                self.label_rank_opt_boss_12,
                self.label_rank_opt_boss_13,
                self.label_rank_opt_boss_14,
            ],
            [
                self.label_rank_opt_dmg_1,
                self.label_rank_opt_dmg_2,
                self.label_rank_opt_dmg_3,
                self.label_rank_opt_dmg_4,
                self.label_rank_opt_dmg_5,
                self.label_rank_opt_dmg_6,
                self.label_rank_opt_dmg_7,
                self.label_rank_opt_dmg_8,
                self.label_rank_opt_dmg_9,
                self.label_rank_opt_dmg_10,
                self.label_rank_opt_dmg_11,
                self.label_rank_opt_dmg_12,
                self.label_rank_opt_dmg_13,
                self.label_rank_opt_dmg_14,
            ],
            [
                self.label_rank_opt_pve_1,
                self.label_rank_opt_pve_2,
                self.label_rank_opt_pve_3,
                self.label_rank_opt_pve_4,
                self.label_rank_opt_pve_5,
                self.label_rank_opt_pve_6,
                self.label_rank_opt_pve_7,
                self.label_rank_opt_pve_8,
                self.label_rank_opt_pve_9,
                self.label_rank_opt_pve_10,
                self.label_rank_opt_pve_11,
                self.label_rank_opt_pve_12,
                self.label_rank_opt_pve_13,
                self.label_rank_opt_pve_14,
            ],
            [
                self.label_rank_opt_pvp_1,
                self.label_rank_opt_pvp_2,
                self.label_rank_opt_pvp_3,
                self.label_rank_opt_pvp_4,
                self.label_rank_opt_pvp_5,
                self.label_rank_opt_pvp_6,
                self.label_rank_opt_pvp_7,
                self.label_rank_opt_pvp_8,
                self.label_rank_opt_pvp_9,
                self.label_rank_opt_pvp_10,
                self.label_rank_opt_pvp_11,
                self.label_rank_opt_pvp_12,
                self.label_rank_opt_pvp_13,
                self.label_rank_opt_pvp_14,
            ],
        ]
        labels_rate = [
            [
                self.label_rank_rate_boss_1,
                self.label_rank_rate_boss_2,
                self.label_rank_rate_boss_3,
                self.label_rank_rate_boss_4,
                self.label_rank_rate_boss_5,
                self.label_rank_rate_boss_6,
                self.label_rank_rate_boss_7,
                self.label_rank_rate_boss_8,
                self.label_rank_rate_boss_9,
                self.label_rank_rate_boss_10,
                self.label_rank_rate_boss_11,
                self.label_rank_rate_boss_12,
                self.label_rank_rate_boss_13,
                self.label_rank_rate_boss_14,
            ],
            [
                self.label_rank_rate_dmg_1,
                self.label_rank_rate_dmg_2,
                self.label_rank_rate_dmg_3,
                self.label_rank_rate_dmg_4,
                self.label_rank_rate_dmg_5,
                self.label_rank_rate_dmg_6,
                self.label_rank_rate_dmg_7,
                self.label_rank_rate_dmg_8,
                self.label_rank_rate_dmg_9,
                self.label_rank_rate_dmg_10,
                self.label_rank_rate_dmg_11,
                self.label_rank_rate_dmg_12,
                self.label_rank_rate_dmg_13,
                self.label_rank_rate_dmg_14,
            ],
            [
                self.label_rank_rate_pve_1,
                self.label_rank_rate_pve_2,
                self.label_rank_rate_pve_3,
                self.label_rank_rate_pve_4,
                self.label_rank_rate_pve_5,
                self.label_rank_rate_pve_6,
                self.label_rank_rate_pve_7,
                self.label_rank_rate_pve_8,
                self.label_rank_rate_pve_9,
                self.label_rank_rate_pve_10,
                self.label_rank_rate_pve_11,
                self.label_rank_rate_pve_12,
                self.label_rank_rate_pve_13,
                self.label_rank_rate_pve_14,
            ],
            [
                self.label_rank_rate_pvp_1,
                self.label_rank_rate_pvp_2,
                self.label_rank_rate_pvp_3,
                self.label_rank_rate_pvp_4,
                self.label_rank_rate_pvp_5,
                self.label_rank_rate_pvp_6,
                self.label_rank_rate_pvp_7,
                self.label_rank_rate_pvp_8,
                self.label_rank_rate_pvp_9,
                self.label_rank_rate_pvp_10,
                self.label_rank_rate_pvp_11,
                self.label_rank_rate_pvp_12,
                self.label_rank_rate_pvp_13,
                self.label_rank_rate_pvp_14,
            ],
        ]
        options = [
            ["공격력 +1", self.calc_pot_ind("공격력", 1)],
            ["공격력 +2", self.calc_pot_ind("공격력", 2)],
            ["공격력 +3", self.calc_pot_ind("공격력", 3)],
            ["보스데미지 +2", self.calc_pot_ind("보스데미지", 2)],
            ["보스데미지 +4", self.calc_pot_ind("보스데미지", 4)],
            ["보스데미지 +6", self.calc_pot_ind("보스데미지", 6)],
            ["회피율 +1", self.calc_pot_ind("회피율", 1)],
            ["회피율 +2", self.calc_pot_ind("회피율", 2)],
            ["회피율 +3", self.calc_pot_ind("회피율", 3)],
            ["도적질 +3", self.calc_pot_ind("도적질", 3)],
            ["도적질 +6", self.calc_pot_ind("도적질", 6)],
            ["도적질 +9", self.calc_pot_ind("도적질", 9)],
            ["치명타데미지 +1", self.calc_pot_ind("치명타데미지", 1)],
            ["치명타데미지 +2", self.calc_pot_ind("치명타데미지", 2)],
            ["치명타데미지 +3", self.calc_pot_ind("치명타데미지", 3)],
            ["치명타확률 +1", self.calc_pot_ind("치명타확률", 1)],
            ["치명타확률 +2", self.calc_pot_ind("치명타확률", 2)],
            ["치명타확률 +3", self.calc_pot_ind("치명타확률", 3)],
            ["스텟 +2", self.calc_pot_ind("스텟", 2)],
            ["스텟 +4", self.calc_pot_ind("스텟", 4)],
            ["스텟 +6", self.calc_pot_ind("스텟", 6)],
            ["포션회복력 +3", self.calc_pot_ind("포션회복력", 3)],
            ["포션회복력 +6", self.calc_pot_ind("포션회복력", 6)],
            ["포션회복력 +9", self.calc_pot_ind("포션회복력", 9)],
            ["스킬시간감소 +1", self.calc_pot_ind("스킬시간감소", 1)],
            ["스킬시간감소 +3", self.calc_pot_ind("스킬시간감소", 3)],
            ["스킬시간감소 +5", self.calc_pot_ind("스킬시간감소", 5)],
            ["운 +5", self.calc_pot_ind("운", 5)],
            ["운 +10", self.calc_pot_ind("운", 10)],
            ["운 +15", self.calc_pot_ind("운", 15)],
            ["방어력 +2", self.calc_pot_ind("방어력", 2)],
            ["방어력 +4", self.calc_pot_ind("방어력", 4)],
            ["방어력 +6", self.calc_pot_ind("방어력", 6)],
            ["명중률 +5", self.calc_pot_ind("명중률", 5)],
            ["명중률 +10", self.calc_pot_ind("명중률", 10)],
            ["명중률 +15", self.calc_pot_ind("명중률", 15)],
            ["자연회복력 +1", self.calc_pot_ind("자연회복력", 1)],
            ["자연회복력 +2", self.calc_pot_ind("자연회복력", 2)],
            ["자연회복력 +3", self.calc_pot_ind("자연회복력", 3)],
            ["평타속도 +2", self.calc_pot_ind("평타속도", 2)],
            ["평타속도 +4", self.calc_pot_ind("평타속도", 4)],
            ["평타속도 +6", self.calc_pot_ind("평타속도", 6)],
        ]
        options_boss = sorted(options, key=lambda x: -x[1][0])
        options_dmg = sorted(options, key=lambda x: -x[1][1])
        options_pve = sorted(options, key=lambda x: -x[1][2])
        options_pvp = sorted(options, key=lambda x: -x[1][3])
        # print(options_boss, options_dmg, options_pve, options_pvp)

        for i in range(14):
            if options_boss[i][1][0] != 0:
                labels_opt[0][i].setPlainText(options_boss[i][0])
                labels_opt[0][i].setAlignment(QtCore.Qt.AlignCenter)
                labels_rate[0][i].setPlainText(
                    str(round(options_boss[i][1][0], 2)) + "%"
                )
                labels_rate[0][i].setAlignment(QtCore.Qt.AlignCenter)
            if options_dmg[i][1][1] != 0:
                labels_opt[1][i].setPlainText(options_dmg[i][0])
                labels_opt[1][i].setAlignment(QtCore.Qt.AlignCenter)
                labels_rate[1][i].setPlainText(
                    str(round(options_dmg[i][1][1], 2)) + "%"
                )
                labels_rate[1][i].setAlignment(QtCore.Qt.AlignCenter)
            if options_pve[i][1][2] != 0:
                labels_opt[2][i].setPlainText(options_pve[i][0])
                labels_opt[2][i].setAlignment(QtCore.Qt.AlignCenter)
                labels_rate[2][i].setPlainText(
                    str(round(options_pve[i][1][2], 2)) + "%"
                )
                labels_rate[2][i].setAlignment(QtCore.Qt.AlignCenter)
            if options_pvp[i][1][3] != 0:
                labels_opt[3][i].setPlainText(options_pvp[i][0])
                labels_opt[3][i].setAlignment(QtCore.Qt.AlignCenter)
                labels_rate[3][i].setPlainText(
                    str(round(options_pvp[i][1][3], 2)) + "%"
                )
                labels_rate[3][i].setAlignment(QtCore.Qt.AlignCenter)

    def calc_pot(self, opt1, value1, opt2, value2, opt3, value3):
        LEVEL = self.LEVEL
        ATK = self.ATK
        DEF = self.DEF
        HP = self.HP
        CRIT_CHANCE = self.CRIT_CHANCE
        CRIT_DMG = self.CRIT_DMG
        DODGE = self.DODGE
        HIT = self.HIT
        MOVE_SPEED = self.MOVE_SPEED
        STAT = self.STAT
        NATURAL_RECOVERY = self.NATURAL_RECOVERY
        POTION_RECOVERY = self.POTION_RECOVERY
        COOLTIME_REDUCE = self.COOLTIME_REDUCE
        ATK_SPEED = self.ATK_SPEED
        LUCK = self.LUCK
        STEAL = self.STEAL
        EXP = self.EXP
        BOSS_DMG = self.BOSS_DMG
        ADDITIONAL_DMG = self.ADDITIONAL_DMG

        if opt1 == "공격력":
            ATK += value1
        elif opt1 == "방어력":
            DEF += value1
        elif opt1 == "치명타확률":
            CRIT_CHANCE += value1
            CRIT_CHANCE = 200 if CRIT_CHANCE > 200 else CRIT_CHANCE
        elif opt1 == "치명타데미지":
            CRIT_DMG += value1
        elif opt1 == "회피율":
            DODGE += value1
            DODGE = 400 if DODGE > 400 else DODGE
        elif opt1 == "명중률":
            HIT += value1
            HIT = 800 if HIT > 800 else HIT
        elif opt1 == "스텟":
            STAT += value1
        elif opt1 == "자연회복력":
            NATURAL_RECOVERY += value1
        elif opt1 == "포션회복력":
            POTION_RECOVERY += value1
        elif opt1 == "스킬시간감소":
            COOLTIME_REDUCE += value1
            COOLTIME_REDUCE = 50 if COOLTIME_REDUCE > 50 else COOLTIME_REDUCE
        elif opt1 == "평타속도":
            ATK_SPEED += value1
        elif opt1 == "운":
            LUCK += value1
        elif opt1 == "도적질":
            STEAL += value1
        elif opt1 == "보스데미지":
            BOSS_DMG += value1

        if opt2 == "공격력":
            ATK += value2
        elif opt2 == "방어력":
            DEF += value2
        elif opt2 == "치명타확률":
            CRIT_CHANCE += value2
            CRIT_CHANCE = 200 if CRIT_CHANCE > 200 else CRIT_CHANCE
        elif opt2 == "치명타데미지":
            CRIT_DMG += value2
        elif opt2 == "회피율":
            DODGE += value2
            DODGE = 400 if DODGE > 400 else DODGE
        elif opt2 == "명중률":
            HIT += value2
            HIT = 800 if HIT > 800 else HIT
        elif opt2 == "스텟":
            STAT += value2
        elif opt2 == "자연회복력":
            NATURAL_RECOVERY += value2
        elif opt2 == "포션회복력":
            POTION_RECOVERY += value2
        elif opt2 == "스킬시간감소":
            COOLTIME_REDUCE += value2
            COOLTIME_REDUCE = 50 if COOLTIME_REDUCE > 50 else COOLTIME_REDUCE
        elif opt2 == "평타속도":
            ATK_SPEED += value2
        elif opt2 == "운":
            LUCK += value2
        elif opt2 == "도적질":
            STEAL += value2
        elif opt2 == "보스데미지":
            BOSS_DMG += value2

        if opt3 == "공격력":
            ATK += value3
        elif opt3 == "방어력":
            DEF += value3
        elif opt3 == "치명타확률":
            CRIT_CHANCE += value3
            CRIT_CHANCE = 200 if CRIT_CHANCE > 200 else CRIT_CHANCE
        elif opt3 == "치명타데미지":
            CRIT_DMG += value3
        elif opt3 == "회피율":
            DODGE += value3
            DODGE = 400 if DODGE > 400 else DODGE
        elif opt3 == "명중률":
            HIT += value3
            HIT = 800 if HIT > 800 else HIT
        elif opt3 == "스텟":
            STAT += value3
        elif opt3 == "자연회복력":
            NATURAL_RECOVERY += value3
        elif opt3 == "포션회복력":
            POTION_RECOVERY += value3
        elif opt3 == "스킬시간감소":
            COOLTIME_REDUCE += value3
            COOLTIME_REDUCE = 50 if COOLTIME_REDUCE > 50 else COOLTIME_REDUCE
        elif opt3 == "평타속도":
            ATK_SPEED += value3
        elif opt3 == "운":
            LUCK += value3
        elif opt3 == "도적질":
            STEAL += value3
        elif opt3 == "보스데미지":
            BOSS_DMG += value3

        result_boss = (
            self.calc_BossStat(
                LEVEL,
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                POTION_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                BOSS_DMG,
            )
            / self.ConvertedStat_Boss
            - 1
        ) * 100
        result_dmg = (
            self.calc_DamageStat(
                ATK,
                STAT,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                BOSS_DMG,
            )
            / self.ConvertedStat_DAMAGE
            - 1
        ) * 100
        result_pve = (
            self.calc_PVEStat(
                LEVEL,
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                POTION_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                LUCK,
                STEAL,
                EXP,
                BOSS_DMG,
            )
            / self.ConvertedStat_PVE
            - 1
        ) * 100
        result_pvp = (
            self.calc_PVPStat(
                ATK,
                STAT,
                HP,
                DEF,
                NATURAL_RECOVERY,
                DODGE,
                CRIT_CHANCE,
                CRIT_DMG,
                COOLTIME_REDUCE,
                ATK_SPEED,
                ADDITIONAL_DMG,
                HIT,
                MOVE_SPEED,
            )
            / self.ConvertedStat_PVP
            - 1
        ) * 100

        return (result_boss, result_dmg, result_pve, result_pvp)

    def sort_pot(self):
        options = [
            ["스킬시간감소 +5", "스킬시간감소", 5],
            ["스킬시간감소 +3", "스킬시간감소", 3],
            ["스킬시간감소 +1", "스킬시간감소", 1],
            ["공격력 +3", "공격력", 3],
            ["공격력 +2", "공격력", 2],
            ["공격력 +1", "공격력", 1],
            ["보스데미지 +6", "보스데미지", 6],
            ["보스데미지 +4", "보스데미지", 4],
            ["보스데미지 +2", "보스데미지", 2],
            ["치명타데미지 +3", "치명타데미지", 3],
            ["치명타데미지 +2", "치명타데미지", 2],
            ["치명타데미지 +1", "치명타데미지", 1],
            ["치명타확률 +3", "치명타확률", 3],
            ["치명타확률 +2", "치명타확률", 2],
            ["치명타확률 +1", "치명타확률", 1],
            ["스텟 +6", "스텟", 6],
            ["스텟 +4", "스텟", 4],
            ["스텟 +2", "스텟", 2],
            ["평타속도 +6", "평타속도", 6],
            ["평타속도 +4", "평타속도", 4],
            ["평타속도 +2", "평타속도", 2],
            ["방어력 +6", "방어력", 6],
            ["방어력 +4", "방어력", 4],
            ["방어력 +2", "방어력", 2],
            ["도적질 +9", "도적질", 9],
            ["도적질 +6", "도적질", 6],
            ["도적질 +3", "도적질", 3],
            ["운 +15", "운", 15],
            ["운 +10", "운", 10],
            ["운 +5", "운", 5],
            ["회피율 +3", "회피율", 3],
            ["회피율 +2", "회피율", 2],
            ["회피율 +1", "회피율", 1],
            ["포션회복력 +9", "포션회복력", 9],
            ["포션회복력 +6", "포션회복력", 6],
            ["포션회복력 +3", "포션회복력", 3],
            ["자연회복력 +3", "자연회복력", 3],
            ["자연회복력 +2", "자연회복력", 2],
            ["자연회복력 +1", "자연회복력", 1],
            ["명중률 +15", "명중률", 15],
            ["명중률 +10", "명중률", 10],
            ["명중률 +5", "명중률", 5],
        ]

        opt1_comb = self.combobox_pot_1.currentText()
        opt2_comb = self.combobox_pot_2.currentText()
        opt3_comb = self.combobox_pot_3.currentText()

        for i in options:
            if opt1_comb == i[0]:
                opt1 = i[1]
                value1 = i[2]
            if opt2_comb == i[0]:
                opt2 = i[1]
                value2 = i[2]
            if opt3_comb == i[0]:
                opt3 = i[1]
                value3 = i[2]
        (boss, dmg, pve, pvp) = self.calc_pot(opt1, value1, opt2, value2, opt3, value3)

        self.label_pot_boss_num.setPlainText(str(round(boss, 2)) + "%")
        self.label_pot_boss_num.setAlignment(QtCore.Qt.AlignCenter)

        self.label_pot_dmg_num.setPlainText(str(round(dmg, 2)) + "%")
        self.label_pot_dmg_num.setAlignment(QtCore.Qt.AlignCenter)

        self.label_pot_pve_num.setPlainText(str(round(pve, 2)) + "%")
        self.label_pot_pve_num.setAlignment(QtCore.Qt.AlignCenter)

        self.label_pot_pvp_num.setPlainText(str(round(pvp, 2)) + "%")
        self.label_pot_pvp_num.setAlignment(QtCore.Qt.AlignCenter)

    def dataload(self):
        if os.path.isfile(file):
            with open(file, "r") as f:
                json_object = json.load(f)
                try:
                    LEVEL = json_object["LEVEL"]
                except:
                    LEVEL = 0
                self.input_level.setPlainText(str(LEVEL))
                self.input_level.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    ATK = json_object["ATK"]
                except:
                    ATK = 0
                self.input_atk.setPlainText(str(ATK))
                self.input_atk.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    DEF = json_object["DEF"]
                except:
                    DEF = 0
                self.input_def.setPlainText(str(DEF))
                self.input_def.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    HP = json_object["HP"]
                except:
                    HP = 0
                self.input_hp.setPlainText(str(HP))
                self.input_hp.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    CRIT_CHANCE = json_object["CRIT_CHANCE"]
                except:
                    CRIT_CHANCE = 0
                self.input_crit_chance.setPlainText(str(CRIT_CHANCE))
                self.input_crit_chance.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    CRIT_DMG = json_object["CRIT_DMG"]
                except:
                    CRIT_DMG = 0
                self.input_crit_dmg.setPlainText(str(CRIT_DMG))
                self.input_crit_dmg.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    DODGE = json_object["DODGE"]
                except:
                    DODGE = 0
                self.input_dodge.setPlainText(str(DODGE))
                self.input_dodge.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    HIT = json_object["HIT"]
                except:
                    HIT = 0
                self.input_hit.setPlainText(str(HIT))
                self.input_hit.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    MOVE_SPEED = json_object["MOVE_SPEED"]
                except:
                    MOVE_SPEED = 0
                self.input_move_speed.setPlainText(str(MOVE_SPEED))
                self.input_move_speed.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    STAT = json_object["STAT"]
                except:
                    STAT = 0
                self.input_stat.setPlainText(str(STAT))
                self.input_stat.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    NATURAL_RECOVERY = json_object["NATURAL_RECOVERY"]
                except:
                    NATURAL_RECOVERY = 0
                self.input_natural_recovery.setPlainText(str(NATURAL_RECOVERY))
                self.input_natural_recovery.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    POTION_RECOVERY = json_object["POTION_RECOVERY"]
                except:
                    POTION_RECOVERY = 0
                self.input_potion_recovery.setPlainText(str(POTION_RECOVERY))
                self.input_potion_recovery.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    COOLTIME_REDUCE = json_object["COOLTIME_REDUCE"]
                except:
                    COOLTIME_REDUCE = 0
                self.input_cooltime_reduce.setPlainText(str(COOLTIME_REDUCE))
                self.input_cooltime_reduce.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    ATK_SPEED = json_object["ATK_SPEED"]
                except:
                    ATK_SPEED = 0
                self.input_atk_speed.setPlainText(str(ATK_SPEED))
                self.input_atk_speed.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    LUCK = json_object["LUCK"]
                except:
                    LUCK = 0
                self.input_luck.setPlainText(str(LUCK))
                self.input_luck.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    STEAL = json_object["STEAL"]
                except:
                    STEAL = 0
                self.input_steal.setPlainText(str(STEAL))
                self.input_steal.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    EXP = json_object["EXP"]
                except:
                    EXP = 0
                self.input_exp.setPlainText(str(EXP))
                self.input_exp.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    BOSS_DMG = json_object["BOSS_DMG"]
                except:
                    BOSS_DMG = 0
                self.input_boss_dmg.setPlainText(str(BOSS_DMG))
                self.input_boss_dmg.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    ADDITIONAL_DMG = json_object["ADDITIONAL_DMG"]
                except:
                    ADDITIONAL_DMG = 0
                self.input_additional_dmg.setPlainText(str(ADDITIONAL_DMG))
                self.input_additional_dmg.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    DMG_A = json_object["DMG_A"]
                except:
                    DMG_A = 0
                self.input_dmg_a.setPlainText(str(DMG_A))
                self.input_dmg_a.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    DMG_B = json_object["DMG_B"]
                except:
                    DMG_B = 0
                self.input_dmg_b.setPlainText(str(DMG_B))
                self.input_dmg_b.setAlignment(QtCore.Qt.AlignCenter)
                try:
                    self.JOB = json_object["JOB"]
                except:
                    self.JOB = 0
                self.combobox_job.setCurrentIndex(self.JOB)
                try:
                    self.NAME = json_object["NAME"]
                except:
                    self.NAME = ""
                self.input_name.setPlainText(str(self.NAME))
                self.input_name.setAlignment(QtCore.Qt.AlignCenter)

        else:
            self.datamake()

    def datamake(self):
        json_object = {
            "LEVEL": 0,
            "ATK": 0,
            "DEF": 0,
            "HP": 0,
            "CRIT_CHANCE": 0,
            "CRIT_DMG": 0,
            "DODGE": 0,
            "HIT": 0,
            "MOVE_SPEED": 0,
            "STAT": 0,
            "NATURAL_RECOVERY": 0,
            "POTION_RECOVERY": 0,
            "COOLTIME_REDUCE": 0,
            "ATK_SPEED": 0,
            "LUCK": 0,
            "STEAL": 0,
            "EXP": 0,
            "BOSS_DMG": 0,
            "ADDITIONAL_DMG": 0,
            "DMG_A": 0,
            "DMG_B": 0,
            "JOB": 0,
            "NAME": "",
        }
        if not os.path.isdir("C:\\ProDays"):
            os.mkdir("C:\\ProDays")
        with open(file, "w") as f:
            json.dump(json_object, f)

    def datasave(self):
        self.button_save.setStyleSheet(
            'background-color: rgb(80, 150, 80);font: 600 18pt "맑은 고딕";color: rgb(255, 255, 255);'
        )
        self.NAME = self.input_name.toPlainText()
        self.JOB = self.combobox_job.currentIndex()

        json_object = {
            "LEVEL": self.LEVEL,
            "ATK": self.ATK,
            "DEF": self.DEF,
            "HP": self.HP,
            "CRIT_CHANCE": self.CRIT_CHANCE,
            "CRIT_DMG": self.CRIT_DMG,
            "DODGE": self.DODGE,
            "HIT": self.HIT,
            "MOVE_SPEED": self.MOVE_SPEED,
            "STAT": self.STAT,
            "NATURAL_RECOVERY": self.NATURAL_RECOVERY,
            "POTION_RECOVERY": self.POTION_RECOVERY,
            "COOLTIME_REDUCE": self.COOLTIME_REDUCE,
            "ATK_SPEED": self.ATK_SPEED,
            "LUCK": self.LUCK,
            "STEAL": self.STEAL,
            "EXP": self.EXP,
            "BOSS_DMG": self.BOSS_DMG,
            "ADDITIONAL_DMG": self.ADDITIONAL_DMG,
            "DMG_A": self.DMG_A,
            "DMG_B": self.DMG_B,
            "JOB": self.JOB,
            "NAME": self.NAME,
        }
        with open(file, "w") as f:
            json.dump(json_object, f)


# 정렬은 이동이 아니라 텍스트수정으로
if __name__ == "__main__":
    version = "v1.6.0"
    # window.title("데이즈 환산스펙 계산기 " + version)
    file = "C:\\ProDays\\PDCVSpec.json"
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
