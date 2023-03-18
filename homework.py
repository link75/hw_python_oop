from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вывести строку сообщения о проведенной тренировке."""
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.')
        return message


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_HOUR = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод нужно определить в дочернем классе!')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * self.get_mean_speed()
                           + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.weight / self.M_IN_KM * self.duration
                           * self.MIN_IN_HOUR)
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float

    CALORIES_WEIGHT_MULTIPLIER_1 = 0.035
    CALORIES_WEIGHT_MULTIPLIER_2 = 0.029
    KMH_TO_MS = 0.278
    HEIGHT_TO_METERS = 100

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        speed_in_ms: float = self.get_mean_speed() * self.KMH_TO_MS
        self.height = self.height / self.HEIGHT_TO_METERS
        calories: float = ((self.CALORIES_WEIGHT_MULTIPLIER_1 * self.weight
                           + (speed_in_ms**2 / self.height)
                           * self.CALORIES_WEIGHT_MULTIPLIER_2
                           * self.weight)
                           * self.duration * self.MIN_IN_HOUR)
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: float

    CALORIES_MEANS_SPEED_MULTIPLIER = 2
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    LEN_STEP = 1.38

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость при плавании."""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        calories: float = ((self.get_mean_speed()
                           + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.CALORIES_MEANS_SPEED_MULTIPLIER
                           * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_classes: dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    if workout_type in training_classes:
        return training_classes[workout_type](*data)

    raise ValueError('Ошибка! Передан неизвестный тип тренировки.')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[float]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
