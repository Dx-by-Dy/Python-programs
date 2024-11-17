import numpy as np
from scipy.stats import f

 
def conf_interval(time_interval, price_shift, p=0.95):
    '''
    Функция для подсчета доверительного интервала с вероятностью p.
    time_interval - массив, состоящий из интервалов времени между трейдами одной стороны, предварительно прологорифмированный.
    price_shift - абсолютные значения смещения цены сделки в трейдах относительно последней известной p_mid и предварительно взятые под корнем,
        то есть sqrt(abs(p_t - p_mid)), где p_t - цена сделки.
    '''

    num_of_obs = len(time_interval)                                                                                   # количество элементов в выборке
    time_mean, price_mean = sum(time_interval) / num_of_obs, sum(price_shift) / num_of_obs                            # считаем средние значения выборки

    variance_time, variance_price, covariance_time_price = 0, 0, 0
    for i in range(num_of_obs):                                                                                       # считаем дисперсии и ковариации выборки
        variance_time += (time_interval[i] - time_mean) ** 2
        variance_price += (price_shift[i] - price_mean) ** 2
        covariance_time_price += (price_shift[i] - price_mean) * (time_interval[i] - time_mean)

    covariance_coef = np.sqrt(variance_time) / np.sqrt(variance_time * variance_price - covariance_time_price ** 2)   # поправочный коэффициент ковариации
    hotelling_stat = np.sqrt(2 * (num_of_obs - 1) / (num_of_obs * (num_of_obs - 2)) * f.ppf(p, 2, num_of_obs - 2))    # статистика Хотеллинга через квантиль распределения Фишера

    return (price_mean - hotelling_stat / covariance_coef) ** 2, (price_mean + hotelling_stat / covariance_coef) ** 2 # итоговый доверительный интервал для смещения p_mid


def full_conf_interval(size_ask, size_bid, conf_interval_ask, conf_interval_bid):
    '''
    Функция связывания результатов доверительных интервалов для ask стороны и bid стороны
    size_ask, size_bid - размеры выборок для ask и bid сторон соответственно, то есть количество трейдов каждой стороны
    conf_interval_ask, conf_interval_bid - доверительные интервалы для ask и bid сторон соответственно 
    '''

    return (size_ask * conf_interval_ask[0] - size_bid * conf_interval_bid[0]) / (size_ask + size_bid),\
            (size_ask * conf_interval_ask[1] - size_bid * conf_interval_bid[1]) / (size_ask + size_bid) # подсчет средневзвешенного соотношения сторон интервалов



# далее код для симуляции входных данных
def gen_data(size, scale_exp, scale_pois):
    time_data = rng.exponential(scale=scale_exp, size=size)
    data_pois = []
    for i in range(size):
        data_pois += [min(rng.poisson(lam=scale_pois / time_data[i], size=1)[0], 10)]
    return time_data, np.array(data_pois)


rng = np.random.default_rng()

size_ask, size_bid = 700, 100
time_data_ask, price_data_ask = gen_data(size_ask, 4, 1)
time_data_bid, price_data_bid = gen_data(size_bid, 5, 0.5)

conf_ask = conf_interval(np.log(time_data_ask), np.sqrt(price_data_ask))
conf_bid = conf_interval(np.log(time_data_bid), np.sqrt(price_data_bid))
full_int = full_conf_interval(size_ask, size_bid, conf_ask, conf_bid)

print(full_int)
print(tuple(np.int16(np.round(full_int))))
